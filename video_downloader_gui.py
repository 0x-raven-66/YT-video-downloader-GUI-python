import PySimpleGUI as sg
from pytube import YouTube
import os


# builtin functions from pytube for the progress bar
def progress_check(stream, chunk, bytes_remaining):
    window['-DOWNLOADPROGRESS-'].update(100 - round(bytes_remaining / stream.filesize * 100))

def on_complete(stream, file_path):
    window['-DOWNLOADPROGRESS-'].update(0)


sg.theme('Darkred1')

# start interface
# one row contain input field and button
# input field will take the url and return its value to pytube object
start_layout = [[sg.Input(key='-INPUT-'), sg.Button('GO', size=(8, 1))]]

# download interface
# contain 3 Frames
download_tab = [
    # frame one contain Video Information in 4 rows
    [sg.Frame('INFORMATION', [[sg.Text('Title:    '), sg.Text('', key='-TITLE-')],
                              [sg.Text('Length:'), sg.Text('', key='-LENGTH-')],
                              [sg.Text('Views: '), sg.Text('', key='-VIEWS-')],
                              [sg.Text('Author:'), sg.Text('', key='-AUTHOR-')]], size=(249, 130), expand_x=True)],

    # frame tow for video contain (Download Button, Resolution, Size) in 2 rows
    [sg.Frame('VIDEO', [
        # 720p
        [sg.Button('Download', size=(16, 2), key='-HIGH-'), sg.Text('720p'),
         sg.Text('', key='-BESTSIZE-')],
        # 360p
        [sg.Button('Download', size=(16, 2), key='-LOW-'), sg.Text('360p'),
         sg.Text('', key='-LOWSIZE-')]], expand_x=True)],

    # frame three for audio contain (Download Button, Extension, Size) in 1 row
    [sg.Frame('AUDIO', [
        [sg.Button('Download', size=(16, 2), key='-AUDIO-'), sg.Text('MP3'),
         sg.Text('', key='-AUDIOSIZE-')]], expand_x=True)],

    # Progress bar in 1 row
    [sg.Progress(100, orientation='h', size=(20, 20), key='-DOWNLOADPROGRESS-', bar_color=('green', 'white'),
                 expand_x=True)]
]
# create folder to download videos in
path = r"D:\downloaded_videos"
if not os.path.exists(path):
    os.makedirs(path)

# start program ...open the input window
window = sg.Window('Youtube Downloader', start_layout)

while True:
    # window.read() to read any actions from user and return them
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    # if user click on GO button
    if event == 'GO':
        # passing input's value to pytube object
        video_object = YouTube(values['-INPUT-'], on_progress_callback=progress_check, on_complete_callback=on_complete)
        # close input window
        window.close()

        # open download window
        window = sg.Window('Youtube Downloader', download_tab, finalize=True)

        # info frame setup
        window['-TITLE-'].update(video_object.title)
        window['-LENGTH-'].update(f'{round(video_object.length / 60, 2)} minutes')
        window['-VIEWS-'].update(video_object.views)
        window['-AUTHOR-'].update(video_object.author)

        # 720p VIDEO frame setup
        # size divided by 1048576 to convert from bytes to megabytes
        window['-BESTSIZE-'].update(f'{round(video_object.streams.get_highest_resolution().filesize / 1048576, 1)} MB')

        # 360p VIDEO frame setup
        # size divided by 1048576 to convert from bytes to megabytes
        window['-LOWSIZE-'].update(f'{round(video_object.streams.get_by_resolution("360p").filesize / 1048576, 1)} MB')

        # AUDIO frame setup
        # size divided by 1048576 to convert from bytes to megabytes
        window['-AUDIOSIZE-'].update(f'{round(video_object.streams.get_audio_only().filesize / 1048576, 1)} MB')

    # if user click on 720p video download button
    if event == '-HIGH-':
        video_object.streams.get_highest_resolution().download(path)
    # if user click on 480p video download button
    if event == '-MID-':
        video_object.streams.get_by_resolution("360p").download(path)
    # if user click on 360p video download button
    if event == '-LOW-':
        video_object.streams.get_by_resolution("360p").download(path)
    # if user click on audio download button
    if event == '-AUDIO-':
        video_object.streams.get_audio_only().download(path)

# close the window if the user click on X
window.close()
