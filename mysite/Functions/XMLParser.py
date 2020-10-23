import xml.etree.ElementTree as ET


def parseXMLwithET():

    tree = ET.parse('../Data/ImputData/annotations.xml')
    root = tree.getroot()
    meta = root.find('meta')
    task = meta[0]
    taskname = task.find('name')
    start_frame = task.find('start_frame')
    stop_frame = task.find('stop_frame')
    tasktext = taskname.text
    start_frame_value = start_frame.text
    stop_frame_value = stop_frame.text
    segments = task.find('segments')
    segment = segments[0]
    segment_start_frame = segment[1].text
    segment_stop_frame = segment[2].text
    task_info = {'taskname': tasktext,
                 'start_frame': start_frame_value,
                 'stop_frame': stop_frame_value,
                 "segment_start": segment_start_frame,
                 "segment_stop": segment_stop_frame}


    frame_info = dict()
    images = root.findall("image")
    for image in images:
        attributes = image.attrib
        if(int(segment_start_frame)<=int(attributes["id"])<=int(segment_stop_frame)):
            boundingboxes = image.findall("box")
            polygons = image.findall("polygon")
            polylines = image.findall("polyline")
            posture_points = image.findall("points")

            image_entities = dict()
            if(len(boundingboxes)!= 0):
                image_entities["boundingboxes"] = boundingboxes
            if(len(polygons)!= 0):
                image_entities["polygons"] = polygons
            if(len(polylines)!= 0):
                image_entities["polylines"] = polylines
            if (len(posture_points) != 0):
                image_entities["posture_points"] = posture_points
            frame_info[attributes["id"]] = image_entities
    return frame_info
