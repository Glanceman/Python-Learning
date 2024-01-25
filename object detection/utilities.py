import torch
from collections import Counter
def intersection_over_union(pred_box,label_box, box_format="midpoint"):
    """
    Video explanation of this function:
    https://youtu.be/XXYG5ZWtjj0

    This function calculates intersection over union (iou) given pred boxes
    and target boxes.

    Parameters:
        pred_box(tensor): Predictions of Bounding Boxes (BATCH_SIZE, 4)
        label_box (tensor): Correct labels of Bounding Boxes (BATCH_SIZE, 4)
        box_format (str): midpoint/corners, if boxes (x,y,w,h) or (x1,y1,x2,y2)

    Returns:
        tensor: Intersection over union for all examples
    """

    if(box_format=="midpoint"):
        #[mid_x,mid_y,width,height]
        box1_x1=pred_box[...,0:1]-pred_box[...,2:3]/2
        box1_y1=pred_box[...,1:2]-pred_box[...,3:4]/2
        box1_x2=pred_box[...,2:3]+pred_box[...,2:3]/2
        box1_y2=pred_box[...,3:4]+pred_box[...,3:4]/2 # shape -> (n,1)
        
        box2_x1=label_box[...,0:1]-label_box[...,2:3]/2
        box2_y1=label_box[...,1:2]-label_box[...,3:4]/2
        box2_x2=label_box[...,2:3]+label_box[...,2:3]/2
        box2_y2=label_box[...,3:4]+label_box[...,3:4]/2

    if(box_format=="corners"):
    # boxs shape = (N,4) (top left -> botton right)
        box1_x1=pred_box[...,0:1]
        box1_y1=pred_box[...,1:2]
        box1_x2=pred_box[...,2:3]
        box1_y2=pred_box[...,3:4] # shape -> (n,1)
        
        box2_x1=label_box[...,0:1]
        box2_y1=label_box[...,1:2]
        box2_x2=label_box[...,2:3]
        box2_y2=label_box[...,3:4]


    x1 = torch.max(box1_x1,box2_x1)
    y1 = torch.max(box1_y1,box2_y1)
    x2 = torch.min(box1_x2,box2_x2)
    y2 = torch.min(box1_y2,box2_y2)

    # clamp 0 is for not intersect -> will have negative
    intersection = (x2-x1).clamp(0)*(y2-y1).clamp(0)

    box1_area= abs((box1_x2- box1_x1)*(box1_y2-box1_y1))
    box2_area= abs((box2_x2- box2_x1)*(box2_y2-box2_y1))

    iou = intersection/ (box1_area+box2_area - intersection +1e-6)
    return iou


def nms(prediction_boxes,prob_threshold ,iou_threshold, box_format="corners"):
    """
        non_max_suppression
        prediction_boxes : list of boxes [[class,probaility,x1,y1,x2,y2],[...],[...]]
    """
    assert type(prediction_boxes)==list
    bboxes= [box for box in prediction_boxes if box[1]>prob_threshold]
    bboxes = sorted(bboxes, key = lambda x:x[1],reverse=True)
    bboxes_after_nms=[]
    
    #nom max suppression
    while bboxes:
        chosen_box= bboxes.pop(0)
        #compare IOU with IOU_threshold for same class
        temp=[]
        for box in bboxes:
            #not same class and less overlapped with same
            iou= intersection_over_union(torch.tensor(chosen_box[2:]),torch.tensor(box[2:]),box_format=box_format)
            if(box[0]!=chosen_box[0] or iou<iou_threshold):
                #keep
                temp.append(box)

        bboxes=temp

        bboxes_after_nms.append(chosen_box)

    return bboxes_after_nms


# ans = nms(
#     [[1,0.9,0,0,1,1],[1,0.7,0.1,0.1,1,1]],
#     0.5,
#     torch.tensor([0.5])
#     )

# print(ans)

def mAP(prediction_boxes,true_boxes,IOU_threshold=0.5,box_format="corner", num_classes=20):
    """
        mean average precision
        prediction_boxes : list of boxes [[img_id,class,probability,x1,y1,x2,y2],[...],[...]]
    """
    average_precision =[]
    epsilon=1e-6
    for c in range(num_classes): #loop each class 
        detections=[]
        ground_truths=[]

        for box in prediction_boxes:
            if(box[1]==c):
                detections.append(box)

        for box in true_boxes:
            if(box[1]==c):
                ground_truths.append(box)
        #img 0 -> 3box
        #img 1 -> 1 box
        #amount_boxes -> {0 $img_id$ :3 $num$,  1:1}
        amount_bboxs = Counter([gt[0] for gt in ground_truths])

        for key, val in amount_bboxs.items():
            #amount_boxes -> {0:torch.tensor([0,0,0]),1:0:torch.tensor([1])}
            amount_bboxs[key]=torch.zeros(val)
        
        #sort by probability 
        detections.sort(key=lambda x:x[2],reverse=True)

        true_positive = torch.zeros(len(detections)) #[0,0,0,0,0]
        false_positive = torch.zeros(len(detections))
        total_true_bboxes = len(ground_truths)

        for detection_id, detection in enumerate(detections): #loop each detection box
            # take truth boxes from the same image
            ground_truth_bboxs_within_same_img = [bbox for bbox in ground_truths if bbox[0]==detection[0] ]
            nums_ground_truth = len(ground_truth_bboxs_within_same_img)

            best_iou=0
            #compare the detection box with the ground truth box
            for index,gt in enumerate(ground_truth_bboxs_within_same_img):
                iou = intersection_over_union(torch.tensor(detection[3:]),torch.tensor(gt[3:]),box_format=box_format)
                if(iou > best_iou):
                    best_iou=iou
                    best_gt_index = index

            if(best_iou > IOU_threshold): # check detection correct?
                if amount_bboxs[detection[0]][best_gt_index]==0:
                    true_positive[detection_id]=1
                    amount_bboxs[detection[0]][best_gt_index]=1
                else: #duplicate box
                    false_positive[detection_id]=1
            else:
                false_positive[detection_id]=1

        #[1,1,0,1,0] -> [1,2,2,3,3]
        true_positive_cumsum= torch.cumsum(true_positive,dim=0)
        false_positive_cumsum=torch.cumsum(false_positive,dim=0)

        recall = true_positive_cumsum/(total_true_bboxes + epsilon)
        precision = torch.divide(true_positive_cumsum,(true_positive_cumsum + false_positive_cumsum + epsilon))
        
        #add starting point 
        recall = torch.cat((torch.tensor([0]),recall)) 
        precision = torch.cat((torch.tensor([1]),precision))
        #intergrate the area
        average_precision.append(torch.trapz(precision,recall))

    return sum(average_precision)/len(average_precision)