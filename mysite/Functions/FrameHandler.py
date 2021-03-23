from mysite.Functions.XMLParser2 import parseXMLwithET, getVideoName
from shutil import copy2, move
from PIL import ImageColor, ImageDraw,Image
import cv2
import os
import mysite.settings as set

objects_information = dict()

all_frames_input_dir = set.MEDIA_ROOT
to_be_annotated_input_dir = set.TO_BE_ANNOTATED
segmentation_dir = set.SEGMENTATION_DIR
bounding_boxes_dir = set.BOUNDING_BOXES_DIR
posture_points_dir = set.POSTURE_POINTS_DIR
annotated_video_dir = set.ANNOTATED_VIDEO
behaviour_annotations_input_dir = set.BEHAVIOUR_ANNOTATIONS_INPUT_DIR
behaviour_annotations_output_dir = set.BEHAVIOUR_ANNOTATIONS_OUTPUT_DIR

def copyAnnotationsFile():
    global all_frames_input_dir, to_be_annotated_input_dir
    src = all_frames_input_dir
    dst = set.INPUT_DATA_DIRECTORY
    srcname = os.path.join(src, 'annotations.xml')
    dstname = os.path.join(dst, 'annotations.xml')
    if os.path.exists(srcname):
        move(srcname, dstname)
    else:
        print("No Annotations File found!")

#will copy the frames to be annotated to "ToBeAnnotated directory"
def copyImagesToBeDisplayedAfterAnnotation():

    global all_frames_input_dir, to_be_annotated_input_dir

    src = all_frames_input_dir
    dst = to_be_annotated_input_dir

    names = os.listdir(src)
    for name in names:
        if(name != 'annotations.xml'):
            srcname = os.path.join(src, name)
            split_name = name.split('_')
            frameName = split_name[1]
            splitFrameName = frameName.split('.')
            frameNumber = str(int(splitFrameName[0]))+'.png'
            dstname = os.path.join(dst, frameNumber)
            copy2(srcname, dstname)
            copy2(srcname, os.path.join(set.ALL_FRAMES,frameNumber))
            copy2(srcname, os.path.join(set.TO_BE_POSTURIZED, frameNumber))
            copy2(srcname, os.path.join(set.BEHAVIOUR_ANNOTATIONS_INPUT_DIR, frameNumber))


def initiateSetupProcess():
    copyImagesToBeDisplayedAfterAnnotation()
    copyAnnotationsFile()
    global objects_information
    objects_information = parseXMLwithET()

#will draw bounding boxes of all objects in that particular frame and save the frame in "OutputData/AnnotatedFrames"
def drawBoundingBoxes():
        global objects_information,to_be_annotated_input_dir, bounding_boxes_dir
        objects = objects_information['boundingboxes']
        labels =  objects_information['labels_info']
        seg_stop = int(objects_information['segment_stop'])

        for obj in objects:
            if type(obj) == int and obj in objects:
                 individual_obj =  objects[obj]
                 for frame in individual_obj:
                     if(type(frame) != str):
                         if (int(frame.attrib['frame']) <= seg_stop) :
                            if frame.attrib['outside'] == '0':
                                image = frame.attrib['frame']
                                top_left = (int(float(frame.attrib['xtl'])), int(float(frame.attrib['ytl'])))
                                bottom_right = (int(float(frame.attrib['xbr'])), int(float(frame.attrib['ybr'])))
                                box_label = objects[obj][len(objects[obj])-1] + str(obj)
                                RGBcolor = ImageColor.getcolor( labels[objects[obj][len(objects[obj])-1]], "RGB")
                                BGRcolor = (RGBcolor[2], RGBcolor[1], RGBcolor[0])
                                impath = os.path.join(to_be_annotated_input_dir,image + ".png")
                                im = cv2.imread(impath.replace("\\", '/'))
                                img = cv2.rectangle(img=im, pt1=top_left, pt2=bottom_right, color=BGRcolor, thickness=1)
                                img = cv2.putText(img,text=box_label,org=top_left,fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=0.5,color=BGRcolor,thickness=1)
                                file = os.path.join(to_be_annotated_input_dir,image + ".png")
                                file = file.replace("\\", '/')
                                cv2.imwrite(file, img)


        names = os.listdir(to_be_annotated_input_dir)
        for name in names:
            srcname = os.path.join(to_be_annotated_input_dir, name)
            dstname = os.path.join(bounding_boxes_dir, name)
            copy2(srcname, dstname)


def makeAnnotatedVideo():
    global annotated_video_dir
    image_folder = set.MEDIA_ROOT
    video_folder = annotated_video_dir
    short_video_name = getVideoName()
    video_name = video_folder+"/"+short_video_name

    sorted_names = []
    for i in range(0,451):
        sorted_names.append(str(i)+'.png')

    frame = cv2.imread(os.path.join(image_folder, sorted_names[0]))
    height, width, layers = frame.shape
    fourcc =cv2.VideoWriter_fourcc(*'MPEG')
    video = cv2.VideoWriter(video_name, fourcc, 30, (width, height))

    for image in sorted_names:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()
    return short_video_name

def makeAnnotatedPostureVideo():
    global annotated_video_dir
    image_folder = set.POSTURE_POINTS_DIR
    video_folder = annotated_video_dir
    short_video_name = getVideoName()
    video_name = video_folder+"/"+short_video_name

    sorted_names = []
    for i in range(0,451):
        sorted_names.append(str(i)+'.png')

    frame = cv2.imread(os.path.join(image_folder, sorted_names[0]))
    height, width, layers = frame.shape
    fourcc =cv2.VideoWriter_fourcc(*'MPEG')
    video = cv2.VideoWriter(video_name, fourcc, 30, (width, height))

    for image in sorted_names:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()
    return short_video_name


def makePosPoints_BoxesVideo():

    filenames = os.listdir(set.BOUNDING_BOXES_DIR)
    for name in filenames:
        srcname = os.path.join(set.BOUNDING_BOXES_DIR, name)
        dstname = os.path.join(set.MERGED_IMAGES_DIR, name)
        copy2(srcname, dstname)

    posture_points = objects_information['posture_points']
    labels = objects_information['labels_info']
    seg_stop = int(objects_information['segment_stop'])
    for point in posture_points:
        if type(point) == int and point in posture_points:
            individual_obj = posture_points[point]
            for frame in individual_obj:
                if (type(frame) != str):
                    if (int(frame.attrib['frame']) <= seg_stop):
                        if frame.attrib['outside'] == '0':
                            image = frame.attrib['frame'] + '.png'
                            im = cv2.imread(os.path.join(set.MERGED_IMAGES_DIR, image))
                            RGBcolor = ImageColor.getcolor(labels[posture_points[point][len(posture_points[point]) - 1]], "RGB")
                            BGRcolor = (RGBcolor[2], RGBcolor[1], RGBcolor[0])
                            x, y = frame.attrib['points'].split(',')
                            x = int(float(x))
                            y = int(float(y))
                            img = cv2.circle(img=im, center=(x, y), radius=3, color=BGRcolor, thickness=-1)
                            cv2.imwrite(os.path.join(set.MERGED_IMAGES_DIR, image), img)

    image_folder = set.MERGED_IMAGES_DIR
    video_folder = set.MERGED_VIDEO_DIR
    short_video_name = getVideoName()
    video_name = video_folder+"/"+ short_video_name

    mergedImagesList = os.listdir(set.MERGED_IMAGES_DIR)
    sorted_names = []
    for i in range(0, len(mergedImagesList)):
       sorted_names.append(str(i) + '.png')

    frame = cv2.imread(os.path.join(image_folder, sorted_names[0]))
    height, width, layers = frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'MPEG')
    video = cv2.VideoWriter(video_name, fourcc, 30, (width, height))

    for image in sorted_names:
       video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()

    mergedImagesList = os.listdir(set.MERGED_IMAGES_DIR)
    for file in mergedImagesList:
       os.remove(os.path.join(set.MERGED_IMAGES_DIR,file))
    return short_video_name


def drawSegmentationPolygons():

    global objects_information, to_be_annotated_input_dir, segmentation_dir
    polygons = objects_information['polygons']
    labels = objects_information['labels_info']
    dest_framename = ''
    src_framename = ''
    imagefile = ''


    for polygon in polygons:
        if type(polygon) == int and polygon in polygons:
            individual_obj = polygons[polygon]
            polygon_label = individual_obj[2]
            obj = individual_obj[0]
            seg_attributes = obj.attrib
            dest_framename = seg_attributes['frame'] + '.png'
            imagefile = os.path.join(set.ALL_FRAMES, seg_attributes['frame'] + '.png')
            if(os.path.isfile(os.path.join(set.TO_BE_SEGMENTED , dest_framename)) != True):
                copy2(imagefile, os.path.join(set.TO_BE_SEGMENTED , dest_framename))

            imagefile = os.path.join(set.TO_BE_SEGMENTED, seg_attributes['frame'] + '.png')
            src_framename = imagefile
            points = str(seg_attributes['points']).split(';')
            RGBcolor = ImageColor.getcolor(labels[polygon_label], "RGB")
            polylines = []
            for point in points:
                x,y = point.split(',')
                x = int(float(x))
                y = int(float(y))
                polylines.append([x,y])
            polylines = tuple(tuple(sub) for sub in polylines)
            im = Image.open(imagefile)
            d = ImageDraw.Draw(im)
            d.polygon(polylines,fill=RGBcolor,outline=(0,0,0))
            im.save(imagefile,quality=100)
    move(src_framename, os.path.join(segmentation_dir,dest_framename))
    return dest_framename


def drawSegmentationPolyLines():
        global objects_information, segmentation_dir
        lanemarkings = objects_information['polylines']

        for marking in lanemarkings:
            individual_obj = lanemarkings[marking]
            line_label = individual_obj[2]
            obj = individual_obj[0]
            line_attributes = obj.attrib
            frame = line_attributes['frame']
            points = str(line_attributes['points']).split(';')
            polylines = []
            for point in points:
                x, y = point.split(',')
                x = int(float(x))
                y = int(float(y))
                polylines.append([x, y])
            linepoints = tuple(tuple(line) for line in polylines)
            im = Image.open(os.path.join(segmentation_dir, frame+'.png'))
            d = ImageDraw.Draw(im)
            d.line(linepoints,fill=(255,255,255),width=1)
            im.save(os.path.join(segmentation_dir, frame+'.png'), quality=100)

def drawPosturePoints():
    global objects_information, to_be_annotated_input_dir, posture_points_dir

    posture_points = objects_information['posture_points']
    labels = objects_information['labels_info']
    seg_stop = int(objects_information['segment_stop'])
    for point in posture_points:
        if type(point) == int and point in posture_points:
            individual_obj = posture_points[point]
            for frame in individual_obj:
                if (type(frame) != str):
                    if ( int(frame.attrib['frame']) <= seg_stop):
                        if frame.attrib['outside'] == '0':
                            image = frame.attrib['frame'] + '.png'
                            im = cv2.imread(os.path.join(set.TO_BE_POSTURIZED, image))
                            RGBcolor = ImageColor.getcolor(labels[posture_points[point][len(posture_points[point]) - 1]], "RGB")
                            BGRcolor = (RGBcolor[2], RGBcolor[1], RGBcolor[0])
                            x,y =  frame.attrib['points'].split(',')
                            x = int(float(x))
                            y = int(float(y))
                            img = cv2.circle(img=im, center=(x, y), radius=3, color=BGRcolor,thickness=-1)
                            cv2.imwrite(os.path.join(set.TO_BE_POSTURIZED, image), img)

    names = os.listdir(set.TO_BE_POSTURIZED)
    for name in names:
        srcname = os.path.join(set.TO_BE_POSTURIZED, name)
        dstname = os.path.join(posture_points_dir, name)
        copy2(srcname, dstname)


def drawSegmentation():
    framenumber = drawSegmentationPolygons()
    drawSegmentationPolyLines()
    return framenumber

def behaviouralAnnotations():
    global objects_information, to_be_annotated_input_dir, bounding_boxes_dir
    objects = objects_information['boundingboxes']
    labels = objects_information['labels_info']
    seg_stop = int(objects_information['segment_stop'])

    for obj in objects:
        if type(obj) == int and obj in objects:
            individual_obj = objects[obj]
            for frame in individual_obj:
                if (type(frame) != str):
                    if (int(frame.attrib['frame']) <= seg_stop):
                        if frame.attrib['outside'] == '0':
                            image = frame.attrib['frame']

def drawBehaviourAnnotations():
    global objects_information, behaviour_annotations_input_dir, behaviour_annotations_output_dir
    objects = objects_information['boundingboxes']
    labels = objects_information['labels_info']
    seg_stop = int(objects_information['segment_stop'])

    for obj in objects:
        if type(obj) == int and obj in objects:
            individual_obj = objects[obj]
            if individual_obj[len(individual_obj)-1] == "pedestrian" :
                for frame in individual_obj:
                        if (type(frame) != str):
                            if (int(frame.attrib['frame']) <= seg_stop):
                                if frame.attrib['outside'] == '0':
                                    image = frame.attrib['frame']

                                    attributes = frame.findall('attribute')
                                    attributes_to_display = list()
                                    for attribute in attributes:
                                        if attribute.text != 'undefined':
                                            attributes_to_display.append(attribute.text)

                                    top_left = (int(float(frame.attrib['xtl'])), int(float(frame.attrib['ytl'])))
                                    bottom_right = (int(float(frame.attrib['xbr'])), int(float(frame.attrib['ybr'])))
                                    RGBcolor = ImageColor.getcolor(labels[objects[obj][len(objects[obj]) - 1]], "RGB")
                                    BGRcolor = (80, 4, 235)
                                    impath = os.path.join(to_be_annotated_input_dir, image + ".png")
                                    im = cv2.imread(impath.replace("\\", '/'))
                                    img = cv2.rectangle(img=im, pt1=top_left, pt2=bottom_right, color=BGRcolor, thickness=2)
                                    file = os.path.join(to_be_annotated_input_dir, image + ".png")
                                    file = file.replace("\\", '/')
                                    cv2.imwrite(file, img)
                                    counter = 0
                                    for att in attributes_to_display:
                                        text_pos = (int(float(frame.attrib['xtl'])), int((float(frame.attrib['ytl'])- 8) - counter))
                                        img = cv2.putText(img, text=att, org=text_pos, fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                                     fontScale=0.6, color=BGRcolor, thickness=2)
                                        file = os.path.join(behaviour_annotations_input_dir, image + ".png")
                                        file = file.replace("\\", '/')
                                        cv2.imwrite(file, img)
                                        counter = counter + 18

    names = os.listdir(behaviour_annotations_input_dir)
    for name in names:
        srcname = os.path.join(behaviour_annotations_input_dir, name)
        dstname = os.path.join(behaviour_annotations_output_dir, name)
        copy2(srcname, dstname)


def makeBehaviourAnnotationsVideo():
    behaviour_annotations_video_dir = set.BEHAVIOUR_ANNOTATIONS_VIDEO_DIR
    image_folder = set.BEHAVIOUR_ANNOTATIONS_OUTPUT_DIR
    video_folder = behaviour_annotations_video_dir
    short_video_name = getVideoName()
    video_name = video_folder + "/" + short_video_name

    sorted_names = []
    for i in range(0, 451):
        sorted_names.append(str(i) + '.png')

    frame = cv2.imread(os.path.join(image_folder, sorted_names[0]))
    height, width, layers = frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'MPEG')
    video = cv2.VideoWriter(video_name, fourcc, 30, (width, height))

    for image in sorted_names:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()
    return short_video_name

if __name__ == '__main__':
    objects_information = parseXMLwithET()
    drawBehaviourAnnotations()



