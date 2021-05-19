import os
from shutil import move, copy2
from zipfile import ZipFile

from django.http import JsonResponse
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from mysite.Functions.FrameHandler import drawBoundingBoxes, makeAnnotatedVideo, \
makeAnnotatedPostureVideo, makePosPoints_BoxesVideo, drawBehaviourAnnotations, makeBehaviourAnnotationsVideo, getListOfVideoFolders
from mysite import settings
from mysite import Functions as func

from mysite.Functions.FrameHandler import initiateSetupProcess

class Home(TemplateView):
    template_name = 'cvat_home.html'

def drawboxes(request):

    drawBoundingBoxes()
    boxes = os.listdir(settings.BOUNDING_BOXES_DIR)
    for file in boxes:
        copy2(os.path.join(settings.BOUNDING_BOXES_DIR, file), os.path.join(settings.MEDIA_ROOT, file))

    filelist = os.listdir(settings.MEDIA_ROOT)

    imagepath = []
    for count in range(0, len(boxes)):
        framenumber = str(count) + '.png'
        counter = filelist[filelist.index(framenumber)]
        imagepath.append("/media/" + counter)

    data = {
        'context': imagepath
    }
    return JsonResponse(data)

def drawPosturePoints(request):

    func.FrameHandler.drawPosturePoints()

    boxes = os.listdir(settings.POSTURE_POINTS_DIR)
    for file in boxes:
        copy2(os.path.join(settings.POSTURE_POINTS_DIR, file), os.path.join(settings.MEDIA_ROOT, file))

    filelist = os.listdir(settings.MEDIA_ROOT)

    imagepath = []
    for count in range(0, len(boxes)):
        framenumber = str(count) + '.png'
        counter = filelist[filelist.index(framenumber)]
        imagepath.append("/media/" + counter)

    data = {
        'context': imagepath
    }
    return JsonResponse(data)


def makeBoundingBoxesVideo(request):

    videoname = makeAnnotatedVideo()
    data = {
        'context': 'Video ' + videoname + ' has been saved!'
    }
    return JsonResponse(data)

def makePostureVideo(request):

    videoname = makeAnnotatedPostureVideo()
    data = {
        'context': 'Video ' + videoname + ' has been saved!'
    }
    return JsonResponse(data)

def makeMergedVideo(request):

    videoname = makePosPoints_BoxesVideo()
    move(os.path.join(settings.MERGED_VIDEO_DIR, videoname), os.path.join(settings.MEDIA_ROOT, videoname))
    data = {
        'filepath': '/media/'+ videoname,
        'filename': videoname
    }
    return JsonResponse(data, safe=False)


def upload(request):
    datas = {}
    if request.method == 'POST':
        import os

        filelist = [f for f in os.listdir(settings.MEDIA_ROOT)]
        for f in filelist:
            os.remove(os.path.join(settings.MEDIA_ROOT, f))

        filelist = [f for f in os.listdir(settings.ALL_FRAMES)]
        for f in filelist:
            os.remove(os.path.join(settings.ALL_FRAMES, f))

        filelist = [f for f in os.listdir(settings.TO_BE_ANNOTATED)]
        for f in filelist:
            os.remove(os.path.join(settings.TO_BE_ANNOTATED, f))

        filelist = [f for f in os.listdir(settings.TO_BE_SEGMENTED)]
        for f in filelist:
            os.remove(os.path.join(settings.TO_BE_SEGMENTED, f))

        filelist = [f for f in os.listdir(settings.TO_BE_POSTURIZED)]
        for f in filelist:
            os.remove(os.path.join(settings.TO_BE_POSTURIZED, f))

        filelist = [f for f in os.listdir(settings.BOUNDING_BOXES_DIR)]
        for f in filelist:
            os.remove(os.path.join(settings.BOUNDING_BOXES_DIR, f))

        filelist = [f for f in os.listdir(settings.MERGED_IMAGES_DIR)]
        for f in filelist:
            os.remove(os.path.join(settings.MERGED_IMAGES_DIR, f))

        filelist = [f for f in os.listdir(settings.POSTURE_POINTS_DIR)]
        for f in filelist:
            os.remove(os.path.join(settings.POSTURE_POINTS_DIR, f))

        filelist = [f for f in os.listdir(settings.SEGMENTATION_DIR)]
        for f in filelist:
            os.remove(os.path.join(settings.SEGMENTATION_DIR, f))

        filelist = [f for f in os.listdir(settings.ANNOTATED_VIDEO)]
        for f in filelist:
            os.remove(os.path.join(settings.ANNOTATED_VIDEO, f))

        filelist = [f for f in os.listdir(settings.MERGED_VIDEO_DIR)]
        for f in filelist:
            os.remove(os.path.join(settings.MERGED_VIDEO_DIR, f))

        filelist = [f for f in os.listdir(settings.BEHAVIOUR_ANNOTATIONS_VIDEO_DIR)]
        for f in filelist:
            os.remove(os.path.join(settings.BEHAVIOUR_ANNOTATIONS_VIDEO_DIR, f))

        filelist = [f for f in os.listdir(settings.BEHAVIOUR_ANNOTATIONS_OUTPUT_DIR)]
        for f in filelist:
            os.remove(os.path.join(settings.BEHAVIOUR_ANNOTATIONS_OUTPUT_DIR, f))

        filelist = [f for f in os.listdir(settings.BEHAVIOUR_ANNOTATIONS_INPUT_DIR)]
        for f in filelist:
            os.remove(os.path.join(settings.BEHAVIOUR_ANNOTATIONS_INPUT_DIR, f))

        request_data = request.POST.get('videos')
        initiateSetupProcess(request_data)

        context = []
        filelist = os.listdir(settings.MEDIA_ROOT)
        for count in range(0, len(filelist)):
            framenumber = str(count) + '.png'
            counter = filelist[filelist.index(framenumber)]
            context.append('/media/' + counter)
        datas = {
            'context': context
        }

    return JsonResponse(datas)


def displaySegmentation(request):
    framenumber = func.FrameHandler.drawSegmentation()
    copy2(os.path.join(settings.SEGMENTATION_DIR, framenumber), os.path.join(settings.MEDIA_ROOT, framenumber))
    context = []
    context.append( '/media/' + framenumber)
    data = {
        'context': context
    }

    return JsonResponse(data)

def exportBoundingBoxes(request):

    videoname = func.FrameHandler.getVideoName()
    zipObj = ZipFile(videoname+'.zip', 'w')

    filelist = os.listdir( settings.BOUNDING_BOXES_DIR )
    for file in filelist:
        zipObj.write(os.path.join(settings.BOUNDING_BOXES_DIR, file), file)
    zipObj.close()

    if(os._exists(os.path.join(settings.MEDIA_ROOT, videoname+'.zip')) == True):
        os.remove(os.path.join(settings.MEDIA_ROOT, videoname+'.zip'))
    move(videoname+'.zip', os.path.join(settings.MEDIA_ROOT, videoname+'.zip'))

    data = {
        'filepath': '/media/' + videoname + '.zip',
        'filename': videoname + '.zip'
    }

    return JsonResponse(data)


def exportPosturePoints(request):

    videoname = func.FrameHandler.getVideoName()
    zipObj = ZipFile(videoname+'.zip', 'w')

    filelist = os.listdir( settings.POSTURE_POINTS_DIR )
    for file in filelist:
        zipObj.write(os.path.join(settings.POSTURE_POINTS_DIR, file), file)
    zipObj.close()

    if(os._exists(os.path.join(settings.MEDIA_ROOT, videoname + '.zip')) == True):
        os.remove(os.path.join(settings.MEDIA_ROOT, videoname + '.zip'))
    move(videoname + '.zip', os.path.join(settings.MEDIA_ROOT, videoname+'.zip'))

    data = {
        'filepath': '/media/' + videoname + '.zip',
        'filename': videoname + '.zip'
    }

    return JsonResponse(data)


def exportSegmentation(request):

    filelist =  os.listdir(settings.SEGMENTATION_DIR)
    seg_frame = ''
    for file in filelist:
        seg_frame = file
    move(os.path.join(settings.SEGMENTATION_DIR, seg_frame), os.path.join(settings.MEDIA_ROOT, seg_frame))

    data = {
        'filepath': '/media/' + seg_frame,
        'filename': seg_frame
    }

    return JsonResponse(data)

def makeBehaviorAnnotationsVideo(request):

    drawBehaviourAnnotations()
    videoname = makeBehaviourAnnotationsVideo()
    data = {
        'context': 'Video ' + videoname + ' has been saved!'
    }
    return JsonResponse(data)

def getListOfVideos(request):
    names = getListOfVideoFolders()
    data = {
        'context': names
    }
    return JsonResponse(data)



