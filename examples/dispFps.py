from timeit import default_timer as timer
import cv2
import subprocess
import time

class DispFps():
    def __init__(self):
        # display variables
        self.__width = 80
        self.__height = 20
        self.__font_size = 0.4
        self.__font_width = 1
        self.__font_style = cv2.FONT_HERSHEY_COMPLEX
        self.__font_color = (255, 255, 255)
        self.__background_color = (0, 0, 0)

        # frame count variables
        self.__frame_count = 0

        # FPS variables
        self.__accum_time = 0
        self.__curr_fps = 0
        self.__prev_time = timer()
        self.__str = "FPS: "

        # CPU temperature variables
        self.__cpu_temperature = 0

        # CPU memory consumption variables
        self.__cpu_mem_consumption = 0

        # GPU memory consumption variables
        self.__gpu_mem_consumption = 0

        # init time
        self.__t0 = time.time()

    def __calc(self):
        # update frame count
        self.__frame_count += 1

        # update FPS
        self.__curr_time = timer()
        self.__exec_time = self.__curr_time - self.__prev_time
        self.__prev_time = self.__curr_time
        self.__accum_time = self.__accum_time + self.__exec_time
        self.__curr_fps = self.__curr_fps + 1
        if self.__accum_time > 1:
            self.__accum_time = self.__accum_time - 1
            self.__str = "FPS: " + str(self.__curr_fps)
            self.__curr_fps = 0

        # update CPU temperature
        command = ["vcgencmd", "measure_temp"]
        result = subprocess.run(command, stdout=subprocess.PIPE)
        tmp = str(result.stdout)
        tmp = tmp.split('=')
        tmp = tmp[1].replace('\\n\"', '')
        self.__cpu_temperature = tmp

        # update CPU memory consumption
        command = ["vcgencmd", "get_mem", "arm"]
        result = subprocess.run(command, stdout=subprocess.PIPE)
        tmp = str(result.stdout)
        tmp = tmp.split('=')
        tmp = tmp[1].replace('\\n\'', '')
        self.__cpu_mem_consumption = tmp

        # update GPU memory consumption
        command = ["vcgencmd", "get_mem", "gpu"]
        result = subprocess.run(command, stdout=subprocess.PIPE)
        tmp = str(result.stdout)
        tmp = tmp.split('=')
        tmp = tmp[1].replace('\\n\'', '')
        self.__gpu_mem_consumption = tmp

    def __disp(self, frame, str, x1, y1, x2, y2):
        cv2.rectangle(frame, (x1, y1), (x2, y2), self.__background_color, -1)
        cv2.putText(frame, str, (x1 + 5, y2 - 5), self.__font_style, self.__font_size, self.__font_color, self.__font_width)

    def disp(self, frame):
        # calculate display contents
        self.__calc()
        # CPU temperature
        # self.__disp(frame, str(self.__frame_count), 0, 0, x2 = self.__width, y2 = self.__height)
        self.__disp(frame, str(self.__cpu_temperature), 0, 0, x2 = self.__width, y2 = self.__height)
        # FPS
        screen_width = int(frame.shape[1])
        self.__disp(frame, self.__str, screen_width - self.__width, 0, screen_width, self.__height)

        # CPU memory consumption
        self.__disp(frame, str(self.__cpu_mem_consumption), 0, self.__height, x2 = self.__width, y2 = self.__height * 2)

        # GPU memory consumption
        self.__disp(frame, str(self.__gpu_mem_consumption), 0, self.__height * 2, x2 = self.__width, y2 = self.__height * 3)

        return time.time() - self.__t0, self.__str, self.__cpu_temperature, self.__cpu_mem_consumption, self.__gpu_mem_consumption