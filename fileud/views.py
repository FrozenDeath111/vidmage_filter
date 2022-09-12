from django.shortcuts import render, HttpResponse
import shortuuid
# import cv2
# import os

from .forms import Iud_form, CBG_form
from .models import file_upload
from .img_proc import *
from .vid_proc import *
from .change_bg import *


# Create your views here.
def index(request):
    return render(request, 'index.html')


def image_process(request):

    if request.method == 'POST':
        client_form = Iud_form(request.POST, request.FILES)
        try:
            option = request.POST['button']
            name = request.session['name']

            filepath = r"./media/" + name
            conv_filepath = r"./media/Converted/cnv_" + name
            img = cv2.imread(filepath)

            if option == 'GreyScale':
                grey_scale(img, conv_filepath)
            elif option == 'Bright':
                bright(img, conv_filepath)
            elif option == 'Darker':
                darker(img, conv_filepath)
            elif option == 'Sharpen':
                sharpen(img, conv_filepath)
            elif option == 'Sepia':
                sepia(img, conv_filepath)
            elif option == 'HDR':
                hdr(img, conv_filepath)
            elif option == 'Inverted':
                inverted(img, conv_filepath)
            elif option == 'GreySketch':
                grey_sketch(img, conv_filepath)
            elif option == 'ColorSketch':
                color_sketch(img, conv_filepath)
            elif option == 'Stylize':
                stylize(img, conv_filepath)
            elif option == 'PencilSketch':
                sketch(img, conv_filepath)
            elif option == 'Summer':
                summer(img, conv_filepath)
            elif option == 'Winter':
                winter(img, conv_filepath)
            else:
                gotham(img, conv_filepath)

            context = {
                'filepath': filepath,
                'conv_filepath': conv_filepath,
                'name': name,
                'img_con': True,
                'on': True
            }
            return render(request, 'img_proc.html', context)

        except:
            if client_form.is_valid():
                files = client_form.cleaned_data['files']
                name = str(files)
                uploaded_name = name

                accepted_list = ['.jpg', '.png']
                name_ext = os.path.splitext(name)[1]
                if name_ext not in accepted_list:
                    return HttpResponse('give supported image file... (jpg, png)')

                name = shortuuid.uuid() + name_ext

                file_upload(file_name=name, img_file=files).save()

                os.rename(r"./media/" + uploaded_name, r"./media/" + name)

                request.session['name'] = name
                filepath = r"./media/"+name
                conv_filepath = r"./media/Converted/cnv_"+name

                context = {
                    'filepath': filepath,
                    'conv_filepath': conv_filepath,
                    'name': name,
                    'img_con': False,
                    'on': True
                }
                return render(request, 'img_proc.html', context)

            else:
                return HttpResponse('error')

    else:
        context = {
            'form': Iud_form(),
            'on': False
        }
        return render(request, 'img_proc.html', context)


def show_file(request):
    return render(request, 'view.html')


def video_process(request):

    if request.method == 'POST':
        client_form = Iud_form(request.POST, request.FILES)

        try:
            option = request.POST['button']
            name = request.session['name']
            size = request.session['size']
            fps = request.session['fps']
            audio_name = request.session['audio_name']

            filename = os.path.splitext(name)[0]
            filework_path = r"./static/temp" + filename + "/"
            filepath = r"./media/" + name
            conv_filepath = r"./media/Converted/" + name

            # print(name, filename, conv_filepath, filework_path, option)

            vid_write(filework_path, conv_filepath, size, fps, option)
            if audio_name != 'not_exist':
                audio_adder(audio_name, conv_filepath, name)
                conv_filepath = r"./media/Converted/cnv_" + name

            context = {
                'filepath': filepath,
                'conv_filepath': conv_filepath,
                'audio_name': audio_name,
                'name': name,
                'vid_con': True,
                'on': True
            }
            return render(request, 'vid_proc.html', context)
        
        except:
            if client_form.is_valid():
                files = client_form.cleaned_data['files']
                name = str(files)
                uploaded_name = name

                accepted_list = ['.mp4']
                name_ext = os.path.splitext(name)[1]
                if name_ext not in accepted_list:
                    return HttpResponse('give supported video file... (.mp4)')

                name = shortuuid.uuid() + name_ext

                file_upload(file_name=name, img_file=files).save()

                os.rename(r"./media/"+uploaded_name, r"./media/"+name)

                request.session['name'] = name
                filepath = r"./media/"+name
                conv_filepath = r"./media/Converted/cnv_"+name

                size, fps = vid_to_frame(filepath, name)
                audio_name = audio_extract(filepath)
                request.session['audio_name'] = audio_name
                request.session['size'] = size
                request.session['fps'] = fps

                context = {
                    'filepath': filepath,
                    'conv_filepath': conv_filepath,
                    'audio_name': audio_name,
                    'name': name,
                    'vid_con': False,
                    'on': True
                }
                return render(request, 'vid_proc.html', context)

            else:
                return HttpResponse('error on vid')

    else:
        context = {
            'form': Iud_form(),
            'on': False
        }
        return render(request, 'vid_proc.html', context)


def change_background(request):
    if request.method == 'POST':
        client_form = CBG_form(request.POST, request.FILES)

        if client_form.is_valid():
            files = client_form.cleaned_data['files']
            file_bg = client_form.cleaned_data['files_bg']
            name = str(files)
            name_bg = str(file_bg)
            uploaded_name = name
            uploaded_name_bg = name_bg

            file_upload(file_name=name, img_file=files).save()
            file_upload(file_name=name, img_file=file_bg).save()

            accepted_list = ['.jpg', '.png']
            name_ext = os.path.splitext(name)[1]
            name_bg_ext = os.path.splitext(name_bg)[1]
            if name_ext not in accepted_list:
                return HttpResponse('give supported image file... (jpg, png)')

            name = shortuuid.uuid() + name_ext
            name_bg = shortuuid.uuid() + name_bg_ext

            os.rename(r"./media/" + uploaded_name, r"./media/" + name)
            os.rename(r"./media/" + uploaded_name_bg, r"./media/" + name_bg)

            filepath = r"./media/" + name
            filepath_bg = r"./media/" + name_bg
            conv_filepath = r"./media/Converted/cnv_" + name

            # try:
            change_bg(filepath, filepath_bg, conv_filepath)
            # except:
                # return HttpResponse('error when converting...')

            context = {
                'filepath': filepath,
                'filepath_bg': filepath_bg,
                'conv_filepath': conv_filepath,
                'on': True
            }
            return render(request, 'change_bg.html', context)

        else:
            return HttpResponse('error')

    else:
        context = {
            'form': CBG_form(),
            'on': False
        }
        return render(request, 'change_bg.html', context)