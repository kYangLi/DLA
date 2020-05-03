#!/usr/bin/python3
#
# Author: Li Yang, liyang6pi5@icloud.com
# Date: 2017.3.2
# Version: 1.2.0
# Usage: python3 main.py
# Descripution: This program is designed for simulating the diffusion-limited 
#                 aggregation(DLA) model. 
#  
# Copyleft LiYang, Physics, THU
#

import random
import tkinter
import numpy as np
import matplotlib.pyplot as plt
import sys
import os


########################
### Class Defination ###
########################
class DlaData:
  kExist = True     # turn the lattice to True if there is a kernal inside
  kNone = False     # turn the lattice to False if there is nothing inside 

  def __init__(self, length, width, 
               init_nuclei_coor_array, enable_periodic_map):
    self.column = length + 2   # total length of the 'game map' (2D array)
    self.row = width + 2       # total width of the 'game map' (2D array)
                               # Setting two more line in the row and column 
                               #   will make it easy to enable the periodic map
    # Patch the nuclei position
    init_nuclei_patch_array = np.ones(
      (len(init_nuclei_coor_array), 
       len(init_nuclei_coor_array[0])),
      dtype=int)
    init_nuclei_coor_array = init_nuclei_coor_array + init_nuclei_patch_array
    self.init_nuclei_coor_array = init_nuclei_coor_array.astype(np.int)
    # If use the periodic map
    self.periodic_map = enable_periodic_map
    # Initial map
    self.map = np.zeros((self.row, self.column), dtype=bool)
    for nuclei_index in range(len(self.init_nuclei_coor_array)):
      ## the self.map array's index must be a TUPLE!!!
      self.map[tuple(self.init_nuclei_coor_array[nuclei_index])] = \
        DlaData.kExist  

  def generate_single_free_kernal(self):
    while True:
      # The free kernal position tuple
      curr_ker_posi = (random.randint(1, self.row-2), 
                       random.randint(1, self.column-2))
      # Refuse to create a free kernal at the lattice 
      #   that already have a kernal inside 
      if self.map[curr_ker_posi]:
        continue           
      # Accpet if the point is valid 
      self.map[curr_ker_posi] = DlaData.kExist
      self.curr_ker_posi = curr_ker_posi
      break          

  def is_stick_to_nuclei(self):
    # Whether the free kernal is stick to the center nuclei
    lattice_up_position = (self.curr_ker_posi[0]-1, self.curr_ker_posi[1])
    lattice_down_position = (self.curr_ker_posi[0]+1, self.curr_ker_posi[1])
    lattice_left_position = (self.curr_ker_posi[0], self.curr_ker_posi[1]-1)
    lattice_right_position = (self.curr_ker_posi[0], self.curr_ker_posi[1]+1)
    # Whether stick to a nuclei
    stick_to_nuclei = self.map[lattice_up_position] or \
                      self.map[lattice_down_position] or \
                      self.map[lattice_left_position] or \
                      self.map[lattice_right_position]
    return stick_to_nuclei
      
  def random_move_free_kernal(self):
    # Move direction set
    move_up = (-1,0)
    move_down = (1,0)
    move_left = (0,-1)
    move_right = (0,1)
    # Random move loop
    while True:
      next_move = random.choice([move_up, move_down, move_left, move_right])
      next_ker_posi = \
        (self.curr_ker_posi[0]+next_move[0], self.curr_ker_posi[1]+next_move[1])
      ## If use the PERIODIC map
      if self.periodic_map:
        ## Current Position
        # Erase the Free Kernal in Current Position
        self.map[self.curr_ker_posi] = DlaData.kNone
        # If current position is at the border, update the value of border, too.
        if self.curr_ker_posi[0] == 1:
          self.map[self.row-1, self.curr_ker_posi[1]] = DlaData.kNone
        elif self.curr_ker_posi[0] == self.row-2:
          self.map[0, self.curr_ker_posi[1]] = DlaData.kNone
        if self.curr_ker_posi[1] == 1:
          self.map[self.curr_ker_posi[0], self.column-1] = DlaData.kNone
        elif self.curr_ker_posi[1] == self.column-2:
          self.map[self.curr_ker_posi[0], 0] = DlaData.kNone
        # It is impossible for the current position getting through the border.
        # Any kernal get through the border will be transported back to the map.
        ## Set Next Position
        # Move the Free Kernal to Next Position
        self.map[next_ker_posi] = DlaData.kExist
        ## Next Position
        # If the next position is at the border
        if next_ker_posi[0] == 1:
          self.map[self.row-1, next_ker_posi[1]] = DlaData.kExist
        elif next_ker_posi[0] == self.row-2:
          self.map[0, next_ker_posi[1]] = DlaData.kExist
        if next_ker_posi[1] == 1:
          self.map[next_ker_posi[0], self.column-1] = DlaData.kExist
        elif next_ker_posi[1] == self.column-2:
          self.map[next_ker_posi[0], 0] = DlaData.kExist  
        # If the next position get through the border, then reset the real posi.
        if next_ker_posi[0] == 0:
          next_ker_posi = (self.row-2, next_ker_posi[1])     
          self.map[next_ker_posi] = DlaData.kExist
        elif next_ker_posi[0] == self.row-1:
          next_ker_posi = (1, next_ker_posi[1])  
          self.map[next_ker_posi] = DlaData.kExist 
        # If nkp[0] eq. to 0 or n-1,
        # then nkp[1] will not eq. to 0 or n-1          
        elif next_ker_posi[1] == 0: 
          next_ker_posi = (next_ker_posi[0],self.column-2)   
          self.map[next_ker_posi] = DlaData.kExist
        elif next_ker_posi[1] == self.column-1:
          next_ker_posi = (next_ker_posi[0], 1) 
          self.map[next_ker_posi] = DlaData.kExist 
        self.curr_ker_posi = next_ker_posi      
      ## If use the APERIODIC map
      else:
        # If the free kernal move out of the border, then refuse.
        if (next_ker_posi[0]<1) or \
          (next_ker_posi[0]>self.row-2) or \
          (next_ker_posi[1]<1) or \
          (next_ker_posi[1]>self.column-2):        
          continue
        # Erase the Free Kernal in Current Position
        self.map[self.curr_ker_posi] = DlaData.kNone
        # Move the Free Kernal to Next Position
        self.map[next_ker_posi] = DlaData.kExist
        # Set Next Position
        self.curr_ker_posi = next_ker_posi
      # End this loop for random move the kernal
      break


# class DlaPltVisual:
#   def __init__(self, array_data):
#     self.data = array_data
#     # Create the figure 
#     self.fig = plt.figure()
#     self.ax = self.fig.add_subplot(111)
#     # Set the font
#     plt.rcParams.update({'font.size': 14,
#                         'font.family': 'STIXGeneral',
#                         'mathtext.fontset': 'stix'})
#     # Set the dpi of the figure 
#     plt.rcParams['figure.dpi'] = 300
#     plt.rcParams['savefig.dpi'] = 300
#     # Set the spacing between the axis and labels
#     plt.rcParams['xtick.major.pad']='8'
#     plt.rcParams['ytick.major.pad']='8'
#     # Set the ticks 'inside' the axis
#     plt.xlabel('')
#     plt.ylabel('')
#     # Set the Ticks of x and y axis
#     plt.xticks([])
#     self.ax.set_xticklabels('')
#     plt.yticks([])
#     self.ax.set_yticklabels('')
#     plt.ylabel('')
#     plt.xlabel('')
#     self.im = self.ax.imshow(self.data, cmap='YlGnBu_r',vmin=0)
#     plt.ion()
#     plt.show()
#
#   def plot_pixel(self):
#     self.im.set_array(self.data)
#     self.fig.canvas.draw()
#     plt.pause(1e-32)


class DlaTkVisual:
  # Zoom ratio of the window in whole screen
  kWindowZoomRatio = 0.9
  def __init__(self, array_data, dla_data_length, dla_data_width):
    ### Set the varible in class DlaTkVisual
    # Size of the data array
    self.data_row_size = len(array_data)     
    self.data_column_size = len(array_data[0])
    self.array_data = array_data
    # Pixel color in different state
    self.color_dict = {DlaData.kNone:'black', DlaData.kExist:'white'}  
    ### Crate the blank window
    self.root = tkinter.Tk()
    self.root.title('DLA Game')            
    ### Set the window size
    size_window_length = \
      self.root.winfo_screenwidth() * DlaTkVisual.kWindowZoomRatio
    size_window_width = \
      self.root.winfo_screenheight() * DlaTkVisual.kWindowZoomRatio
    ### Calculate the single pixel size
    pixel_length = size_window_length / float(dla_data_length + 2)
    pixel_width = size_window_width / float(dla_data_width + 2)
    pixel_size = min(pixel_length, pixel_width)
    self.pixel_size = int(pixel_size)
    ### Update the window size
    size_window_length = size_window_length * self.pixel_size / pixel_length
    size_window_width = size_window_width * self.pixel_size / pixel_width
    ### Set the window at the center of the screen
    windows_position_info = \
      '%dx%d+%d+%d' %(size_window_length, size_window_width, 
                      (self.root.winfo_screenwidth() - size_window_length)/2, 
                      (self.root.winfo_screenheight() - size_window_width)/2)
    self.root.geometry(windows_position_info) 
    ### Set the Canvas 
    self.canvas = tkinter.Canvas(self.root, bg = 'black')
    self.init_canvas()
    self.canvas.pack()   
    self.canvas.config(width=size_window_length, height=size_window_width)

  def init_canvas(self):
    # A 2d list for saving every handle of 'canvas rectangle'
    self.grid_handle = list() 
    # Plot the border line of canvas
    self.canvas.create_rectangle(0, 0, self.pixel_size*(self.data_row_size), 
                                       self.pixel_size*(self.data_column_size),
                                       fill='gray',
                                       outline='gray')                
    # Plot every pixel in the canvas by 'for' cycle
    for row_num in range(1, self.data_row_size-1):                    
      self.grid_handle.insert(row_num-1,list())
      # Plot index: 1 to data_size-2 (in 0 to data_size-1)
      for column_num in range(1, self.data_column_size-1):            
        self.grid_handle[row_num-1].insert(column_num-1,
          self.canvas.create_rectangle(
            self.pixel_size*column_num, 
            self.pixel_size*row_num,
            self.pixel_size*(column_num+1), 
            self.pixel_size*(row_num+1),
            fill=self.color_dict[self.array_data[row_num][column_num]],
            outline=self.color_dict[self.array_data[row_num][column_num]]))

  def plot_pixel(self):
    # Use itemconfig to change the color of every canvas rectangle
    # Plot every pixel in the canvas by 'for' cycle
    for row_num in range(1, self.data_row_size-1):  
      # plot index: 1 to data_size-2 (in 0 to data_size-1)              
      for column_num in range(1, self.data_column_size-1):        
        self.canvas.itemconfig(
          self.grid_handle[row_num-1][column_num-1],
          fill=self.color_dict[self.array_data[row_num][column_num]],
          outline=self.color_dict[self.array_data[row_num][column_num]]) 
    self.canvas.update()    

###############################
### Sub Function Defination ###
###############################
def int_input_consider_default(show_str, defalut_value):
  # integer input reads considering the default value
  input_str = str(input(show_str))
  if '' == input_str:
    is_int_num = False
  else:
    is_int_num = True
  for str_element in range(len(input_str)):
    is_int_num = is_int_num and (ord(input_str[str_element])>=ord('0') \
                                 and ord(input_str[str_element])<=ord('9'))
    if not is_int_num:
      break
  if is_int_num:
    get_value = int(input_str)
  else:
    get_value = defalut_value
  return get_value


def player_guide_interface():
  print("                                                               ")
  print("                                                               ")
  print("           oooooooooo.        ooooo                  .o.       ")
  print("           888     888b.      '888'                 .888.      ")
  print("           888       888b.     888                 .8:888.     ")
  print("           888       8888.     888                .8' '888.    ")
  print("           888       888p.     888               .88ooo8888.   ")
  print("           888     888p.      '8888888888b      .8'     '888.  ")
  print("           888888888o         o88888888888o    o88o     o8888o ")
  print("                                                               ")
  print("                                                               ")
  print("               Diffusion-limited Aggregation(DLA) Model        ")
  print("                         Simulation Program                    ")
  print("                                                               ")
  print("                   LiYang (liyang6pi5@icloud.com)              ")
  print("                     Last Update Date: 2017.3.1                ")
  print("                           Version: 1.2.0                      ")
  print("                        Python3 Support Only                   ")
  print("                      Copyleft liyang@phys.thu                 ")
  print("                                                               ")

  while True:
    print("  ")
    print("******************************")
    print("* Set the Basic Parameter... *")
    print("******************************")
    # Observe way
    print('Observe the pattern of each step in the evolution?(Y/[N]/D)')
    print("> 'Y' : 'Yes, enable the step by step observation, please!'")
    print("> 'N' : 'No, thanks. Just show the final pattern of each kernal.'")
    print("> 'D' : 'What? No, I even do not want to see the output window!")
    print(">        JUST OUTPUT THE DATA FILE! Understand?'")
    input_str = str(input('>>> '))
    observe_every_evolution = False
    data_file_only_mode = False
    if ('Y' == input_str) or ('y' == input_str):
      observe_every_evolution = True
      print('+--------------------------------------------------------------+')
      print('|!!! BE ATTENTION !!!                                          |')
      print('|                                                              |')
      print('|Opening this "observation" function may led to a slow MEMORY  |') 
      print('|  LEAK, and seriously reduce the calculating speed.           |')
      print('|  Strongly suggest that DO NOT open this function,            |')
      print('|  unless the 2D Data Array Length is less that 50.            |')
      print('+--------------------------------------------------------------+')
    elif ('D' == input_str) or ('d' == input_str):
        data_file_only_mode = True
      
    # Periodic boundary
    print('')
    print('Use periodic boundary condition or not?(Y/[N])')
    input_str = str(input('>>> '))
    if ('Y' == input_str) or ('y' == input_str):
      enable_periodic_map = True
    else:
      enable_periodic_map = False
    # Set the default parameter
    if observe_every_evolution:
      kernal_num = 100
      dla_data_length = 20
      dla_data_width = 20
    else:
      if enable_periodic_map:
        kernal_num = 80000
        dla_data_length = 500
        dla_data_width = 500
      else:
        kernal_num = 80000
        dla_data_length = 500
        dla_data_width = 500
    init_nuclei_coor_array = \
      np.array(((dla_data_width/2-1, dla_data_length/2-1),))
    init_nuclei_num = len(init_nuclei_coor_array)
    # Print default parameters list
    print('   ')
    print(' DEFAULT PARAMETER LIST:')
    print('|--------------------------------------')
    print('| 2D Data Array Width:      %d' % dla_data_width)
    print('| 2D Data Array Length:     %d' % dla_data_length)
    print('| Kernal Number:            %d' % kernal_num) 
    print('| Init Nuclei Number:       %d' % init_nuclei_num) 
    for init_nuclei_index in range(init_nuclei_num):
      if not init_nuclei_index:
        print('| Init Nuclei Coordinate:   (%d,%d)' 
              % (init_nuclei_coor_array[init_nuclei_index,0],
                 init_nuclei_coor_array[init_nuclei_index,1]))
      else:
        print('|                           (%d,%d)' 
              % (init_nuclei_coor_array[init_nuclei_index,0],
                 init_nuclei_coor_array[init_nuclei_index,1]))
    print('|--------------------------------------') 
    # If change the default value
    print('Change the DEFAULT parameter?(Y/[N])')
    change_defult_parameter = str(input('>>> '))
    if ('Y' == change_defult_parameter) or  ('y' == change_defult_parameter):
      # Array Width
      print('Please input the 2D Data Array Width:')
      dla_data_width = int_input_consider_default('>>> ', dla_data_width)
      # Array Length
      print('Please input the 2D Data Array Length:')
      dla_data_length = int_input_consider_default('>>> ', dla_data_length)
      # Total Kernal Number
      print('Please input the Kernal Number:')
      kernal_num = int_input_consider_default('>>> ', kernal_num) 
      while kernal_num > dla_data_width * dla_data_length:
        print('> !!!The input Kernal Number is too large!!!')
        print('Try again, please:')
        kernal_num = int_input_consider_default('>>> ', kernal_num) 
      # Init Nuclei Number
      print('Please input the Init Nuclei Number:')
      init_nuclei_num = int_input_consider_default('>>> ', init_nuclei_num)
      # Create the init. nuclei list array with known size
      init_nuclei_coor_array = \
        np.array([init_nuclei_coor_array[0] for row in range(init_nuclei_num)])
      print('Please input the Init Nuclei Coordinate:')
      print('> Input one by one, in the form of:')
      print('> "position_in_width,position_in_length"')
      print('> For example: >>> 199,199')
      for init_nuclei_index in range(init_nuclei_num):
        str_init_nuclei_coors = \
          str(input('#%d >>> ' % (init_nuclei_index+1)))
        # If do not input anything, keep default value
        if '' != str_init_nuclei_coors:        
          for str_index in range(len(str_init_nuclei_coors)):
            if ord(str_init_nuclei_coors[str_index])<ord('0') or \
               ord(str_init_nuclei_coors[str_index])>ord('9'):
              break
          init_nuclei_coordinate_x = int(str_init_nuclei_coors[:str_index])
          init_nuclei_coordinate_y = int(str_init_nuclei_coors[str_index+1:])
          init_nuclei_coordinate = \
            np.array((init_nuclei_coordinate_x, init_nuclei_coordinate_y))
          init_nuclei_coor_array[init_nuclei_index] = init_nuclei_coordinate
        # CHECK if the init nuclei's position is out of range
        if init_nuclei_coor_array[init_nuclei_index][0] > dla_data_width:
          init_nuclei_coor_array[init_nuclei_index] = \
            (dla_data_width-1, init_nuclei_coor_array[init_nuclei_index][1])
        if init_nuclei_coor_array[init_nuclei_index][1] > dla_data_length:
          init_nuclei_coor_array[init_nuclei_index] = \
            (init_nuclei_coor_array[init_nuclei_index][0], dla_data_length-1)
    # Parameters list Check
    print("  ")
    print("****************************")
    print("* Basic Parameter Check!!! *")
    print("****************************")
    print(' BASIC PARAMETER LIST:')
    print('|--------------------------------------')
    print('| Data File Only Mode:      %s' % data_file_only_mode)
    print('| Observe Every Evolution:  %s' % observe_every_evolution)
    print('| Use Periodic Lattice:     %s' % enable_periodic_map)
    print('| 2D Data Array Width:      %d' % dla_data_width)
    print('| 2D Data Array Length:     %d' % dla_data_length)
    print('| Max Kernal Number:        %d' % (dla_data_width*dla_data_length))
    print('| Set Kernal Number:        %d' % kernal_num)
    print("| Kernal Occupancy:         %.1f %%" 
          % (float(kernal_num)/(dla_data_width*dla_data_length)*100))
    print('| Init Nuclei Number:       %d' % init_nuclei_num) 
    for init_nuclei_index in range(init_nuclei_num):
      if not init_nuclei_index:
        print('| Init Nuclei Coordinate:   (%d,%d)' 
              % (init_nuclei_coor_array[init_nuclei_index,0],
                 init_nuclei_coor_array[init_nuclei_index,1]))
      else:
        print('|                           (%d,%d)' 
              % (init_nuclei_coor_array[init_nuclei_index,0],
                 init_nuclei_coor_array[init_nuclei_index,1]))
    print('|--------------------------------------') 
    # If reset the parameters
    print(' ')
    print("[( ' -')]Start the evolution?([Y]/N)")
    print("[\\(>_<)\\]> 'Y' : 'Yeah, let's roll!'")
    print("[(¯^¯ ) ]> 'N' : 'No, I’d like to reset some parameters...'")
    print('')
    reset_parameter = str(input('>>> '))
    if ('N' == reset_parameter) or ('n' == reset_parameter):
      pass
    else:
      if not data_file_only_mode:
        print(" ")
        print('The new observe window has been created...')
      break
  print('  ')
  print("*******************************")
  print("* Caluculation in Progress... *")
  print("*******************************") 
  return kernal_num, dla_data_length, dla_data_width, \
         observe_every_evolution,data_file_only_mode, \
         enable_periodic_map, init_nuclei_coor_array


def print_processing_bar(finished_count, all_count):
  ### print the processing bar of the calculation
  kProcessBarLength = 50
  finished_count = finished_count - 1
  process_percent = int(float(finished_count) / all_count * 1000)/10.0
  process_bar_num = int(kProcessBarLength * process_percent / 100)
  process_bar = '#' * process_bar_num + \
                ' ' * (kProcessBarLength - process_bar_num)
  process_print = '[' + process_bar + ']' + str(finished_count) + \
                  '/' + str(all_count) + ' ====>> ' + str(process_percent) + '%'
  delete_print = '\b' * len(process_print)
  # Print process bar
  sys.stdout.write(process_print)
  sys.stdout.flush()
  sys.stdout.write(delete_print)


def plt_heat_plot(filename_pic, matrix, pic_dpi, pic_format):
  ## DIY figure
  fig = plt.figure(figsize=(5,5))
  ax = fig.add_subplot(111)
  # Set the font
  plt.rcParams.update({'font.size': 14,
                       'font.family': 'STIXGeneral',
                       'mathtext.fontset': 'stix'})
  # Set the spacing between the axis and labels
  plt.rcParams['xtick.major.pad']='8'
  plt.rcParams['ytick.major.pad']='8'
  # Set the ticks 'inside' the axis
  plt.xlabel('')
  plt.ylabel('')
  # Set the Ticks of x and y axis
  plt.xticks([])
  ax.set_xticklabels('')
  plt.yticks([])
  ax.set_yticklabels('')
  plt.ylabel('')
  plt.xlabel('')
  ## Plot
  ax.imshow(matrix, cmap='YlGnBu_r',vmin=0)
  ## Save the figure
  plt.savefig(filename_pic, format=pic_format, dpi=pic_dpi)


def dla_data_saved(enable_periodic_map, dla_data_length, dla_data_width,
                   kernal_num, init_nuclei_coor_array, dla_data,
                   final_position_data_sum, pic_dpi, pic_format):
  # Enter the data file
  if not os.path.isdir("./data"):
    os.makedirs("./data")
  os.chdir("./data")
  # Data filename 
  if enable_periodic_map:
    tag = '[periodic]'
  else:
    tag = '[aperiodic]'
  filename_arraydata = str(dla_data_length) + 'X' + str(dla_data_width) + \
                       '-' + str(kernal_num) + '-' + \
                       str(len(init_nuclei_coor_array)) + \
                       '-' + tag + '.mat'
  filename_plotdata = str(dla_data_length) + 'X' + str(dla_data_width) + \
                      '-' + str(kernal_num) + '-' + \
                      str(len(init_nuclei_coor_array)) + \
                      '-' + tag + '.dat'
  filename_pic = str(dla_data_length) + 'X' + str(dla_data_width) + \
                 '-' + str(kernal_num) + '-' + \
                 str(len(init_nuclei_coor_array)) + \
                 '-' + tag + '.' + pic_format
  # Data saving
  print('  ')
  print("***************************")
  print("****   Data Saving...  ****")
  print("***************************")
  np.savetxt(filename_arraydata, dla_data.map, fmt="%d")
  print("'*.dlaarray' data file created successfully!")
  print('> This data file record the fianl 2D data array of DLA.')
  print('')
  np.savetxt(filename_plotdata, final_position_data_sum, fmt="%d")
  print("'*.dlaplot' data file created successfully!")
  print('> You could use this data file to plot tha pattern of DLA ')
  print('> by using other plot software, such as GNUPLOT.')
  print('')
  plt_heat_plot(filename_pic, dla_data.map, pic_dpi, pic_format)
  print(' DATA FILE LIST:')
  print('|--------------------------------------------------------------------')
  print('| Array Data File Name:      ./data/%s' % filename_arraydata)
  print('| Coordinate Data File Name: ./data/%s' % filename_plotdata)
  print('| Final Pattern:             ./data/%s' % filename_pic)
  print('|--------------------------------------------------------------------')
  print('>>> Data Saved!!! <<<')


def program_complete():
  print('')
  print('>>> Program Complete! <<<')
  print('Quitting...')
  print('')


#####################
### Main Function ###
#####################
def main():
  ### Start the Player Guide Interface ###
  kernal_num, dla_data_length, dla_data_width, \
  observe_every_evolution, data_file_only_mode, \
  enable_periodic_map, init_nuclei_coor_array = player_guide_interface()
  ### DLA Data Part Set ###
  dla_data = DlaData(dla_data_length, dla_data_width, 
                     init_nuclei_coor_array, enable_periodic_map)
  ### DLA Plot Part Set ###
  if not data_file_only_mode:
    dla_plot = DlaTkVisual(dla_data.map, dla_data_length, dla_data_width)
  ### Evolution Calculation START ###
  # 2D array to save the point coordinate of the final pattern
  final_position_data_sum = np.zeros((kernal_num,2), dtype=int) 
  # free kernal generate and random move loop   
  for step_index in range(1,kernal_num+1):
    dla_data.generate_single_free_kernal()
    # step by step observation switch I
    if not data_file_only_mode:
      dla_plot.plot_pixel()
    # processing bar print
    print_processing_bar(step_index, kernal_num)
    while not dla_data.is_stick_to_nuclei():
      dla_data.random_move_free_kernal()
      # step by step observation switch II
      if observe_every_evolution:
        dla_plot.plot_pixel()
    # output the kernal final state 
    if (not observe_every_evolution) and (not data_file_only_mode):    
      dla_plot.plot_pixel()
    # save the point coordinate of the final pattern
    final_position_data_sum[step_index-1,:] = dla_data.curr_ker_posi
  print_processing_bar(kernal_num+1, kernal_num)
  print('')
  print(">>> Calculation Complete!!! <<<")
  ### Data Save ###
  dla_data_saved(enable_periodic_map, dla_data_length, dla_data_width,
                 kernal_num, init_nuclei_coor_array, dla_data,
                 final_position_data_sum, 400, 'png')
  ### Quit Program ###
  program_complete()


#################
### Exec Part ###
#################
if __name__ == '__main__':
  main()


#----------------------------------------------#
#            PROGRAM HISTORY LOG               #
#----------------------------------------------#
# 2017.2.25  *** PROJECT OPEN ***
#
# 2017.2.26  *** Version 1.0.0 EXPRESS ***
#
# 2017.2.27  ADD: The periodic map 
#            ADD: The multiple initial nuclei
#            *** Version 1.0.2 EXPRESS ***
#
# 2017.2.28  FIX: Periodic support - 2D data assignment bug fix.
#                 Bug : self.map[self.row-1, :] = self.map[1, :]
#                 Fix : self.map[self.row-1, 1:self.column-2] = \
#                       self.map[1, 1:self.column-2]
#            DELETE: Delete the FIX upon and abandon the algorithm of 
#                      PERIODIC before 
#            UPDATE: Update the algorithm of PERIODIC MAP 
#            ADD: Border lines in canvas
#            ADD: Input check function
#            *** Version 1.1.0 EXPRESS ***
#
# 2017.2.29  UPDATE: The dla_data_saved function's parameter transport.
#            FIX:  Some spell error
#            ADD:  Init Nuclei Coordinate input check
#            ADD:  Bash script to run the main code
#            ADD:  Non-plot mode
#            *** Version 1.1.1 EXPRESS ***
#  
# 2017.3.1  UPDATE:  Update the init nuclei coordinate set divided symbol 
#           *** Version 1.1.1 EXPRESS ***
#
# 2017.3.2  ADD: Figure output from matplotlib  
#           *** Version 1.2.0 EXPRESS ***
#
# 2017.3.2  *** PROJECT CLOSED ***
# 
#
