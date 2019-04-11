#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-
#
# Please using python 2.7 run this code
# 
# This program is a simulation of Diffusion-limited Aggregation(DLA) model 
# 
# liyang6pi5@icloud.com
# Copyleft liyang JLU Physics 2018
 
from Tkinter import *
import random
import numpy as np
import sys


#######################################################
#================ CLASS DEFINED =======================
#######################################################

class DlaData:
  kExist = True                                  # turn the lattice to True if there is a kernel inside
  kNone = False                                  # turn the lattice to False if there is nothing inside 

  def __init__(self, length, width, init_nuclei_data_array, enable_periodic_map):
    self.column = length + 2                     # total length of the 'game map' (2D array)
    self.row = width + 2                         # total width of the 'game map' (2D array)
                                                 # Setting two more line in the row and column 
                                                 #   will make it easy to enable the periodic map
    # patch the nuclei position
    init_nuclei_patch_array = np.ones((len(init_nuclei_data_array),
                                       len(init_nuclei_data_array[0])),dtype=int)                     
    init_nuclei_data_array = init_nuclei_data_array + init_nuclei_patch_array
    self.init_nuclei_array = init_nuclei_data_array

    self.periodic_map = enable_periodic_map
    
    #self.map = [[0 for index_length in range(self.length)] for index_width in range(self.width)]
    self.map = np.zeros((self.row, self.column), dtype=bool)

    for init_nuclei_index in range(len(self.init_nuclei_array)):
      ## the self.map array's index must be a TUPLE!!!
      self.map[tuple(self.init_nuclei_array[init_nuclei_index])] = DlaData.kExist  

  def generate_single_free_kernel(self):
    while True:
      free_kernel_position =(random.randint(1, self.row-2), 
                             random.randint(1, self.column-2))
                                                 # the free kernel position tuple
      if self.map[free_kernel_position]:
        continue                                 # refuse to create a free kernel at the lattice 
                                                 #   that already have a kernel inside 
      
      self.map[free_kernel_position] = DlaData.kExist
      self.free_kernel = free_kernel_position
      break          

  def is_stick_to_nuclei(self):
    # whether the free kernel is stick to the center nuclei
    lattice_up_position = (self.free_kernel[0]-1, self.free_kernel[1])
    lattice_down_position = (self.free_kernel[0]+1, self.free_kernel[1])
    lattice_left_position = (self.free_kernel[0], self.free_kernel[1]-1)
    lattice_right_position = (self.free_kernel[0], self.free_kernel[1]+1)

    stick_to_nuclei = self.map[lattice_up_position] or \
                      self.map[lattice_down_position] or \
                      self.map[lattice_left_position] or \
                      self.map[lattice_right_position]
       
    return stick_to_nuclei
      
  def random_move_free_kernel(self):
    ## move direction set
    move_up = (-1,0)
    move_down = (1,0)
    move_left = (0,-1)
    move_right = (0,1)

    while True:
      next_move = random.choice([move_up, move_down, move_left, move_right])
      free_kernel_next_position = (self.free_kernel[0]+next_move[0], self.free_kernel[1]+next_move[1])

      ### if use the PERIODIC map
      if self.periodic_map:            
        ## if the free kernel move out of the border, then refuse. (Periodic)
        if (free_kernel_next_position[0]<0) or \
          (free_kernel_next_position[0]>self.row-1) or \
          (free_kernel_next_position[1]<0) or \
          (free_kernel_next_position[1]>self.column-1):       
          continue

        ## Finishing the Move in 2D Data Array(Use Periodic Map)
        # Erase the Free Kernel in Current Position
        self.map[self.free_kernel] = DlaData.kNone
        # Move the Free Kernel to Next Position
        self.map[free_kernel_next_position] = DlaData.kExist
        
        ## Current Position
        # if current position is at the border
        if self.free_kernel[0] == 1:
          self.map[self.row-1, self.free_kernel[1]] = DlaData.kNone
        elif self.free_kernel[0] == self.row-2:
          self.map[0, self.free_kernel[1]] = DlaData.kNone
        else:
          pass
        if self.free_kernel[1] == 1:
          self.map[self.free_kernel[0], self.column-1] = DlaData.kNone
        elif self.free_kernel[1] == self.column-2:
          self.map[self.free_kernel[0], 0] = DlaData.kNone
        else:
          pass

        # It is impossible for the current position getting through the border...
        # Any kernel get through the border will be transported back to the map 
        #   at the last of this method!
        
        ## Set Next Position
        self.free_kernel = free_kernel_next_position

        ## Next Position
        ## DO NOT change the 'if' judge order, 
        ##   or coordinate(0,1) will make mistake in calculation!!!
        # if the next position is at the border
        if free_kernel_next_position[0] == 1:
          self.map[self.row-1, free_kernel_next_position[1]] = DlaData.kExist
        elif free_kernel_next_position[0] == self.row-2:
          self.map[0, free_kernel_next_position[1]] = DlaData.kExist
        else:
          pass
        if free_kernel_next_position[1] == 1:
          self.map[free_kernel_next_position[0], self.column-1] = DlaData.kExist
        elif free_kernel_next_position[1] == self.column-2:
          self.map[free_kernel_next_position[0], 0] = DlaData.kExist  
        else:
          pass
        # if the next position get through the border
        if free_kernel_next_position[0] == 0:
          self.free_kernel = (self.row-2, free_kernel_next_position[1])     #set the new legal position
          self.map[self.free_kernel] = DlaData.kExist
        elif free_kernel_next_position[0] == self.row-1:
          self.free_kernel = (1, free_kernel_next_position[1])  
          self.map[self.free_kernel] = DlaData.kExist                   
        elif free_kernel_next_position[1] == 0:
          self.free_kernel = (free_kernel_next_position[0],self.column-2)   
          self.map[self.free_kernel] = DlaData.kExist
        elif free_kernel_next_position[1] == self.column-1:
          self.free_kernel = (free_kernel_next_position[0], 1) 
          self.map[self.free_kernel] = DlaData.kExist 
        # in the gerneral case            
        else:
          pass
               
      ###if use the APERIODIC map
      else:      
        ##if the free kernel move out of the border, then refuse.
        if (free_kernel_next_position[0]<1) or \
          (free_kernel_next_position[0]>self.row-2) or \
          (free_kernel_next_position[1]<1) or \
          (free_kernel_next_position[1]>self.column-2):        
          continue
        
        ## Finishing the Move in 2D Data Array(Use APeriodic Map)
        # Erase the Free Kernel in Current Position
        self.map[self.free_kernel] = DlaData.kNone
        # Move the Free Kernel to Next Position
        self.map[free_kernel_next_position] = DlaData.kExist
        # Set Next Position
        self.free_kernel = free_kernel_next_position
      
      break

class ArrayPlot:
  kWindowZoomRatio = 0.9                                               # zoom ratio of the window in whole screen

  def __init__(self, array_data):
    ### set the varible in class ArrayPlot
    self.data_row_size = len(array_data)                               # size of the data array
    self.data_column_size = len(array_data[0])
    self.array_data = array_data
    self.color_dict = {DlaData.kNone:'black', DlaData.kExist:'white'}  # pixel color in different state
    
    ### crate the blank window
    self.root = Tk()
    self.root.title('DLA Game')            

    ### set the window size
    size_window_length = self.root.winfo_screenwidth() * ArrayPlot.kWindowZoomRatio
    size_window_width = self.root.winfo_screenheight() * ArrayPlot.kWindowZoomRatio

    ### calculate the single pixel size
    pixel_length = size_window_length / float(dla_data_length + 2)
    pixel_width = size_window_width / float(dla_data_width + 2)
    pixel_size = min(pixel_length, pixel_width)
    self.pixel_size = int(pixel_size)

    ### update the window size
    size_window_length = size_window_length * self.pixel_size / pixel_length
    size_window_width = size_window_width * self.pixel_size / pixel_width

    ### set the window at the center of the screen
    windows_position_info = '%dx%d+%d+%d' \
                            %(size_window_length, 
                              size_window_width, 
                              (self.root.winfo_screenwidth() - size_window_length) / 2, 
                              (self.root.winfo_screenheight() - size_window_width) / 2)    
    self.root.geometry(windows_position_info) 

    ### set the canvas 
    self.canvas = Canvas(self.root, bg = 'black')
    self.init_canvas()
    self.canvas.pack()   
    self.canvas.config(width=size_window_length, height=size_window_width)


  def init_canvas(self):
    self.grid_handle = list()                                         # A 2d list for saving every handle of 'canvas rectangle'

    self.canvas.create_rectangle(0, 0, self.pixel_size*(self.data_row_size), 
                                       self.pixel_size*(self.data_column_size),
                                       fill='gray',
                                       outline='gray')                # plot the border line of canvas

    for row_num in range(1, self.data_row_size-1):                    # plot every pixel in the canvas by 'for' cycle
      self.grid_handle.insert(row_num-1,list())

      for column_num in range(1, self.data_column_size-1):            # plot index: 1 to data_size-2 (in 0 to data_size-1)
        self.grid_handle[row_num-1].insert(column_num-1,
          self.canvas.create_rectangle(self.pixel_size*column_num, 
                                       self.pixel_size*row_num,
                                       self.pixel_size*(column_num+1), 
                                       self.pixel_size*(row_num+1),
                                       fill=self.color_dict[self.array_data[row_num][column_num]],
                                       outline=self.color_dict[self.array_data[row_num][column_num]]))

  def plot_pixel(self):
    # use itemconfig to change the color of every canvas rectangle
    for row_num in range(1, self.data_row_size-1):                # plot every pixel in the canvas by 'for' cycle
      for column_num in range(1, self.data_column_size-1):        # plot index: 1 to data_size-2 (in 0 to data_size-1)
        self.canvas.itemconfig(self.grid_handle[row_num-1][column_num-1],
                               fill=self.color_dict[self.array_data[row_num][column_num]],
                               outline=self.color_dict[self.array_data[row_num][column_num]]) 
    self.canvas.update()    

#######################################################
#========== LITTLE FUNCRION DEFINED ===================
#######################################################

def int_input_consider_default(show_str, defalut_value):
  ###integer input reads considering the default value
  input_str = raw_input(show_str)
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
  print("                                                             ")
  print("                                                             ")
  print("           oooooooooo.        ooooo                  .o.      ")
  print("           888     888b.      '888'                 .888.     ")
  print("           888       888b.     888                 .8:888.    ")
  print("           888       8888.     888                .8' '888.   ")
  print("           888       888p.     888               .88ooo8888.  ")
  print("           888     888p.      '8888888888b      .8'     '888. ")
  print("           888888888o         o88888888888o    o88o     o8888o")
  print("                                                             ")
  print("                                                             ")
  print("               Diffusion-limited Aggregation(DLA) Model ")
  print('                         Simulation Program')
  print(' ')
  print("                   LiYang (liyang6pi5@icloud.com)")
  print("                     Last Update Date: 2018.3.1 ")
  print("                           Version: 1.2.0")
  print("                        Copyleft liyang@JPAs")
  print("                                                            ")

  while True:
    print("  ")
    print("******************************")
    print("* Set the Basic Parameter... *")
    print("******************************")
    print('Observe the Pattern of Every Step in the Evolution(Y/N/D):')
    print("> 'Y' : 'Yes, enable the step by step observation, please!'")
    print("> 'N' : 'No, thanks. Just show me the final pattern in a window'")
    print("> 'D' : 'What? No, I even do not want to see the output window!")
    print(">        JUST OUTPUT A DATA FILE! Understand?'")
    observe_every_evolution = raw_input('>>> ')
    data_file_only_mode = False
    if ('Y' == observe_every_evolution) or ('y' == observe_every_evolution):
      observe_every_evolution = True
      print('+----------------------------------------------------------------+')
      print('|BE ATTENTION!!!                                                 |')
      print('|                                                                |')
      print('|Opening this observation function may led to a slow MEMORY LEAK,|') 
      print('|and seriously reduce the calculating speed.                     |')
      print('|Strongly suggest that DO NOT open this function,                |')
      print('|unless the 2D Data Array Length is less that 50.                |')
      print('+----------------------------------------------------------------+')   
    else:
      if ('D' == observe_every_evolution) or ('d' == observe_every_evolution):
        data_file_only_mode = True
        
      observe_every_evolution = False

    print('  ')
    print('Use periodic boundary condition or not?(Y/N)')
    enable_periodic_map = raw_input('>>> ') 
    if ('Y' == enable_periodic_map) or ('y' == enable_periodic_map):
      enable_periodic_map = True
    else:
      enable_periodic_map = False
    
    ### set the default parameter
    if observe_every_evolution:
      kernel_num = 10
      dla_data_length = 20
      dla_data_width = 20
    else:
      if enable_periodic_map:
        kernel_num = 10000
        dla_data_length = 200
        dla_data_width = 200
      else:
        kernel_num = 32000
        dla_data_length = 400
        dla_data_width = 400

    init_nuclei_array = np.array(((dla_data_width/2 - 1, dla_data_length/2 - 1),))
    init_nuclei_num = len(init_nuclei_array)

    print('   ')
    print(' DEFAULT PARAMETER LIST:')
    print('|--------------------------------------')
    print('| 2D Data Array Width:      %d' % dla_data_width)
    print('| 2D Data Array Length:     %d' % dla_data_length)
    print('| Kernel Number:            %d' % kernel_num) 
    print('| Init Nuclei Number:       %d' % init_nuclei_num) 
    for init_nuclei_list_index in range(init_nuclei_num):
      if not init_nuclei_list_index:
        print('| Init Nuclei Coordinate:   (%d,%d)' % (init_nuclei_array[init_nuclei_list_index,0],
                                                       init_nuclei_array[init_nuclei_list_index,1]))
      else:
        print('|                           (%d,%d)' % (init_nuclei_array[init_nuclei_list_index,0],
                                                       init_nuclei_array[init_nuclei_list_index,1]))
    print('|--------------------------------------') 
    print('Change the DEFAULT parameter?(Y/N)')
    change_defult_parameter = raw_input('>>> ')

    if ('Y' == change_defult_parameter) or  ('y' == change_defult_parameter):
      print('Please input the 2D Data Array Width:')
      dla_data_width = int_input_consider_default('>>> ', dla_data_width)

      print('Please input the 2D Data Array Length:')
      dla_data_length = int_input_consider_default('>>> ', dla_data_length)

      print('Please input the Kernel Number:')
      kernel_num = int_input_consider_default('>>> ', kernel_num) 
      while kernel_num > dla_data_width * dla_data_length:
        print('> !!!The input Kernel Number is too large!!!')
        print('Try again, please:')
        kernel_num = int_input_consider_default('>>> ', kernel_num) 

      print('Please input the Init Nuclei Number:')
      init_nuclei_num = int_input_consider_default('>>> ', init_nuclei_num)
      
      init_nuclei_array = np.array([init_nuclei_array[0] for row in range(init_nuclei_num)])
                                                          #crate the init nuclei list array with known size
      print('Please input the Init Nuclei Coordinate:')
      print('> Input one by one, in the form of:')
      print('> "position_in_width,position_in_length"')
      print('> For example: >>> 199,199')
      for init_nuclei_list_index in range(init_nuclei_num):
        init_nuclei_array_char = raw_input('#%d >>> ' % (init_nuclei_list_index+1))
        if '' != init_nuclei_array_char:        # if do not input anything, keep default value
          #init_nuclei_array_char_index = init_nuclei_array_char.find(',')
          for init_nuclei_array_char_index in range(len(init_nuclei_array_char)):
            if ord(init_nuclei_array_char[init_nuclei_array_char_index])<ord('0') or \
               ord(init_nuclei_array_char[init_nuclei_array_char_index])>ord('9'):
              break
          init_nuclei_coordinate_x = int(init_nuclei_array_char[:init_nuclei_array_char_index])
          init_nuclei_coordinate_y = int(init_nuclei_array_char[init_nuclei_array_char_index+1:])
          init_nuclei_coordinate = np.array((init_nuclei_coordinate_x, init_nuclei_coordinate_y))
          init_nuclei_array[init_nuclei_list_index] = init_nuclei_coordinate
        #CHECK if the init nuclei's position is out of range
        if init_nuclei_array[init_nuclei_list_index][0] > dla_data_width:
          init_nuclei_array[init_nuclei_list_index] = (dla_data_width-1, init_nuclei_array[init_nuclei_list_index][1])
        if init_nuclei_array[init_nuclei_list_index][1] > dla_data_length:
          init_nuclei_array[init_nuclei_list_index] = (init_nuclei_array[init_nuclei_list_index][0], dla_data_length-1)

    print("  ")
    print("*******************************")
    print("* Basic Parameter Checking!!! *")
    print("*******************************")
    print(' BASIC PARAMETER LIST:')
    print('|--------------------------------------')
    print('| Data File Only Mode:      %s' % data_file_only_mode)
    print('| Observe Every Evolution:  %s' % observe_every_evolution)
    print('| Use Periodic Lattice:     %s' % enable_periodic_map)
    print('| 2D Data Array Width:      %d' % dla_data_width)
    print('| 2D Data Array Length:     %d' % dla_data_length)
    print('| Max Kernel Number:        %d' % (dla_data_width*dla_data_length))
    print('| Set Kernel Number:        %d' % kernel_num)
    print("| Kernel Occupancy:         %.1f %%" % (float(kernel_num)/(dla_data_width*dla_data_length)*100))
    print('| Init Nuclei Number:       %d' % init_nuclei_num) 
    for init_nuclei_list_index in range(init_nuclei_num):
      if not init_nuclei_list_index:
        print('| Init Nuclei Coordinate:   (%d,%d)' % (init_nuclei_array[init_nuclei_list_index,0],
                                                       init_nuclei_array[init_nuclei_list_index,1]))
      else:
        print('|                           (%d,%d)' % (init_nuclei_array[init_nuclei_list_index,0],
                                                       init_nuclei_array[init_nuclei_list_index,1]))
    print('|--------------------------------------') 
    print(' ')
    print("[( ' -')]Start the evolution?(Y/N)")
    print("[\(>_<)\]> 'Y' : 'Yeah, let's roll!'")
    print("[(¯^¯ ) ]> 'N' : 'No, I’d like to reset some parameters...'")
    print(' ')

    reset_parameter = raw_input('>>> ')
    if ('N' == reset_parameter) or ('n' == reset_parameter):
      pass
    else:
      if observe_every_evolution:
        print(" ")
        print('The new observe window has been create!!!')
      break

  print('  ')
  print("******************************")
  print("* Caluculation Processing... *")
  print("******************************")
    
  return kernel_num, dla_data_length, dla_data_width, \
         observe_every_evolution,data_file_only_mode, \
         enable_periodic_map, init_nuclei_array


def print_processing_bar(finished_count, all_count):
  ###print the processing bar of the calculation
  kProcessBarLength = 50
  finished_count = finished_count - 1
  process_percent = int(float(finished_count) / all_count * 1000)/10.0
  process_bar_num = int(kProcessBarLength * process_percent / 100)
  process_bar = '#' * process_bar_num + ' ' * (kProcessBarLength - process_bar_num)

  process_print = '[' + process_bar + ']' + str(finished_count) +'/' + str(all_count) +\
                  ' ====>> ' + str(process_percent) + '%'
  delete_print = '\b' * len(process_print)

  sys.stdout.write(process_print)
  sys.stdout.flush()
  sys.stdout.write(delete_print)


def dla_data_saved(): 
  if enable_periodic_map:
    filename_arraydata = str(dla_data_length)+'X'+str(dla_data_width)+\
                         '-'+str(kernel_num)+'-'+str(len(init_nuclei_array))+'-[periodic].dlaarray'
    filename_plotdata = str(dla_data_length)+'X'+str(dla_data_width)+\
                         '-'+str(kernel_num)+'-'+str(len(init_nuclei_array))+'-[periodic].dlaplot'
  else:
    filename_arraydata = str(dla_data_length)+'X'+str(dla_data_width)+\
                         '-'+str(kernel_num)+'-'+str(len(init_nuclei_array))+'-[aperiodic].dlaarray'
    filename_plotdata = str(dla_data_length)+'X'+str(dla_data_width)+\
                        '-'+str(kernel_num)+'-'+str(len(init_nuclei_array))+'-[aperiodic].dlaplot'

  print('  ')
  print("***************************")
  print("****   Data Saving...  ****")
  print("***************************")
  np.savetxt(filename_arraydata, dla_data.map, fmt="%d")
  print("'xxx.dlaarray' data file created successfully!")
  print('> This data file record the fianl 2D data array of DLA.')
  print('             ')
  np.savetxt(filename_plotdata, final_position_data_sum, fmt="%d")
  print("'xxx.dlaplot' data file created successfully!")
  print('> You could use this data file to plot tha pattern of DLA ')
  print('> by using other plot software, such as GNUPLOT.')
  print('               ')
  print(' DATA FILE LIST:')
  print('|-------------------------------------------------------------')
  print('| Array Data File Name:         %s' % filename_arraydata)
  print('| Coordinate Data File Name:    %s' % filename_plotdata)
  print('|-------------------------------------------------------------')
  print('>>> Data Saved!!! <<<')


def program_complete():
  print('  ')
  print('>>> Program Complete! <<<')
  print('Quitting...')
  print('  ')

#######################################################
#==================== MAIN CODE =======================
#######################################################
if __name__ == '__main__':
  #****Start the Player Guide Interface****
  kernel_num, dla_data_length, dla_data_width, \
  observe_every_evolution, data_file_only_mode, \
  enable_periodic_map, init_nuclei_array = player_guide_interface()
  
  #****DLA Data Part Set ****
  dla_data = DlaData(dla_data_length, dla_data_width, init_nuclei_array, enable_periodic_map)

  #****DLA Plot Part Set****
  if not data_file_only_mode:
    dla_plot = ArrayPlot(dla_data.map)

  #****Evolution Calculation START****
  # 2D array to save the point coordinate of the final pattern
  final_position_data_sum = np.zeros((kernel_num,2), dtype=int) 
  # free kernel generate and random move loop   
  for step_index in range(1,kernel_num+1):
    dla_data.generate_single_free_kernel()
    # step by step observation switch I
    if observe_every_evolution:
      dla_plot.plot_pixel()
    #processing bar print
    print_processing_bar(step_index, kernel_num)
    
    while not dla_data.is_stick_to_nuclei():
      dla_data.random_move_free_kernel()
      # step by step observation switch II
      if observe_every_evolution:
        dla_plot.plot_pixel()

    # save the point coordinate of the final pattern
    final_position_data_sum[step_index-1,:] = dla_data.free_kernel 
  
  print_processing_bar(kernel_num+1, kernel_num)
  print('')
  print(">>> Calculation Complete!!! <<<")

  #****Output the Final Pattern****
  if (not observe_every_evolution) and (not data_file_only_mode):    
    print('     ')
    print("***************************")
    print("**** Pattern Output... ****")
    print("***************************")
    print('Final Pattern is creating...')
    dla_plot.plot_pixel()
    print('>>> Final Pattern is create!!! <<<')
  
  #****Tkinter Mainloop****
  if not data_file_only_mode:
    print('  ')
    print('> Close the Pattren Output Window to save the calculate data.')
    dla_plot.canvas.mainloop()     

  #****Data Save****
  dla_data_saved()
  
  #****Quit Program****
  program_complete()


#----------------------------------------------#
###########  PROGRAM HISTORY LOG  ##############
#----------------------------------------------#
# 2018.2.25  Program coding Start
#
# 2018.2.26  *** Version 1.0.0 EXPRESS ***
#
# 2018.2.27  ADD: The periodic map 
#            ADD: The multiple initial nuclei
#            *** Version 1.0.2 EXPRESS ***
#
# 2018.2.28  FIX: Periodic support - 2D data assignment bug fix.
#                 Bug : self.map[self.row-1, :] = self.map[1, :]
#                 Fix : self.map[self.row-1, 1:self.column-2] = self.map[1, 1:self.column-2]
#            DELETE: Delete the FIX upon and abandon the algorithm of PERIODIC before 
#            UPDATE: Update the algorithm of PERIODIC MAP 
#            ADD: Border lines in canvas
#            ADD: Input check function
#            *** Version 1.1.0 EXPRESS ***
#
# 2018.2.29  UPDATE: The dla_data_saved function's parameter transport.
#            FIX:  Some spell error
#            ADD:  Init Nuclei Coordinate input check
#            ADD:  Bash script to run the main code
#            ADD:  Non-plot mode
#            *** Version 1.1.1 EXPRESS ***
#  
# 2018.3.1  UPDATE:  Update the init nuclei coordinate set divided symbol 
#           *** Version 1.1.1 EXPRESS ***
# *END*
