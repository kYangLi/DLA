#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
#Please using python 2.7 run this code
#
#This program is a simulation of Diffusion-limited Aggregation(DLA) model
#liyang6pi5@icloud.com
#copy left liyang JLU Physics 2014
 
from Tkinter import *
import random
import numpy as np
#from time import sleep
import sys


#######################################################
#================ CLASS DEFINED =======================
#######################################################

class DlaData:
  kExist = True                                  #turn the lattice to True if there is a kernel inside
  kNone = False                                  #turn the lattice to False if there is nothing inside 

  def __init__(self, length, width, init_nuclei_data_array, enable_periodic_map):
    self.colnum = length + 2                     #total length of the 'game map' (2D array)
    self.row = width + 2                         #total width of the 'game map' (2D array)
                                                 #setting two more line in the row and colnum 
                                                 #make it easy to enable the periodic map
    #patch the nuclei position
    init_nuclei_patch_array = np.ones((len(init_nuclei_data_array),
                                       len(init_nuclei_data_array[0])),dtype=int)                     
    init_nuclei_data_array = init_nuclei_data_array + init_nuclei_patch_array
    self.init_nuclei_array = init_nuclei_data_array

    self.periodic_map = enable_periodic_map
    
    #self.map = [[0 for index_length in range(self.length)] for index_width in range(self.width)]
    self.map = np.zeros((self.row, self.colnum), dtype=bool)

    for init_nuclei_index in range(len(self.init_nuclei_array)):
      ##the self.map array's index must be a tuple!!!
      self.map[tuple(self.init_nuclei_array[init_nuclei_index])] = DlaData.kExist  

  def generate_single_free_kernel(self):
    while True:
      free_kernel_position =(random.randint(1, self.row-2), 
                             random.randint(1, self.colnum-2))
                                                 #the free kernel position tuple
      if self.map[free_kernel_position]:
        continue                                 #refuse to create a free kernel at the lattice 
                                                 #point that already have a kernel inside 
      
      self.map[free_kernel_position] = DlaData.kExist
      self.free_kernel = free_kernel_position
      break          

  def is_stick_to_nuclei(self):
    #whether the free kernel is stick to the center nuclei
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
    ##move direction 
    move_up = (-1,0)
    move_down = (1,0)
    move_left = (0,-1)
    move_right = (0,1)

    while True:
      next_move = random.choice([move_up, move_down, move_left, move_right])
      free_kernel_next_position = (self.free_kernel[0]+next_move[0], self.free_kernel[1]+next_move[1])

      ###if use the PERIODIC map
      if self.periodic_map:            
        ##if the free kernel move out of the border, then refuse. (Periodic)
        if (free_kernel_next_position[0]<0) or \
          (free_kernel_next_position[0]>self.row-1) or \
          (free_kernel_next_position[1]<0) or \
          (free_kernel_next_position[1]>self.colnum-1):       
          continue

        ##finishing the move in 2D data array(use periodic map)
        #erase the free kernel
        self.map[self.free_kernel] = False
        #update the border
        self.map[self.row-1, :] = self.map[1, :]
        self.map[0, :] = self.map[self.row-2, :] 
        self.map[:, self.colnum-1] = self.map[:, 1]
        self.map[:, 0] = self.map[:, self.colnum-2]
        #move the free kernel to next position
        self.map[free_kernel_next_position] = True
        ##check the periodic map data change at border
        self.map[1, :] = self.map[self.row-1, :]
        self.map[self.row-2, :] = self.map[0, :]
        self.map[:, 1] = self.map[:, self.colnum-1]
        self.map[:, self.colnum-2] = self.map[:, 0]
        
        ##enable the periodic border movement
        if free_kernel_next_position[0] == 0:
          #set the free_kernel_next_position[0] to row-2
          free_kernel_next_position = (self.row - 2, free_kernel_next_position[1])  
        elif free_kernel_next_position[0] == self.row-1:
          #set the free_kernel_next_position[0] to 1
          free_kernel_next_position = (1, free_kernel_next_position[1])                     
        elif free_kernel_next_position[1] == 0:
          #set the free_kernel_next_position[1] to colnum-2
          free_kernel_next_position = (free_kernel_next_position[0],self.colnum - 2)   
        elif free_kernel_next_position[1] == self.colnum-1:
          #set the free_kernel_next_position[1] to 1
          free_kernel_next_position = (free_kernel_next_position[0], 1)                
        else:
          pass
               
        self.free_kernel = free_kernel_next_position
        #self.map[self.free_kernel] = True


      ###if use the APERIODIC map
      else:      
        ##if the free kernel move out of the border, then refuse.
        if (free_kernel_next_position[0]<1) or \
          (free_kernel_next_position[0]>self.row-2) or \
          (free_kernel_next_position[1]<1) or \
          (free_kernel_next_position[1]>self.colnum-2):        
          continue
        
        ##finishing the move in 2D data array
        self.map[free_kernel_next_position] = True
        self.map[self.free_kernel] = False
        self.free_kernel = free_kernel_next_position
      
      break

class ArrayPlot:
  kWindowZoomRatio = 0.9                                               #zoom ratio of the window in whole screen

  def __init__(self, array_data):
    ###set the varible in class ArrayPlot
    self.data_row_size = len(array_data)                               #size of the data array
    self.data_column_size = len(array_data[0])
    self.array_data = array_data
    self.color_dict = {DlaData.kNone:'white', DlaData.kExist:'black'}  #pixel color in different state
    
    ###crate the blank window
    self.root = Tk()
    self.root.title('DLA Game')            

    ###set the window size
    size_window_length = self.root.winfo_screenwidth() * ArrayPlot.kWindowZoomRatio
    size_window_width = self.root.winfo_screenheight() * ArrayPlot.kWindowZoomRatio

    ###calculate the single pixel size
    pixel_length = size_window_length / float(dla_data_length + 2)
    pixel_width = size_window_width / float(dla_data_width + 2)
    pixel_size = min(pixel_length, pixel_width)
    self.pixel_size = int(pixel_size)

    ###update the window size
    size_window_length = size_window_length * self.pixel_size / pixel_length
    size_window_width = size_window_width * self.pixel_size / pixel_width

    ###set the window at the center of the screen
    windows_position_info = '%dx%d+%d+%d' \
                            %(size_window_length, 
                              size_window_width, 
                              (self.root.winfo_screenwidth() - size_window_length) / 2, 
                              (self.root.winfo_screenheight() - size_window_width) / 2)    
    self.root.geometry(windows_position_info) 

    ###set the canvas 
    self.canvas = Canvas(self.root, bg = 'white')
    self.init_canvas()
    self.canvas.pack()   
    self.canvas.config(width=size_window_length, height=size_window_width)


  def init_canvas(self):
    self.grid_handle = list()                                         #A 2d list for saving every handle of 'canvas rectangle'

    for row_num in range(1, self.data_row_size-1):                    #plot every pixel in the canvas by 'for' cycle
      self.grid_handle.insert(row_num-1,list())

      for column_num in range(1, self.data_column_size-1):            #plot index: 1 to data_size-2 (in 0 to data_size-1)
        self.grid_handle[row_num-1].insert(column_num-1,
          self.canvas.create_rectangle(self.pixel_size*(column_num+1), 
                                       self.pixel_size*(row_num+1),
                                       self.pixel_size*(column_num+2), 
                                       self.pixel_size*(row_num+2),
                                       fill=self.color_dict[self.array_data[row_num][column_num]],
                                       outline=self.color_dict[self.array_data[row_num][column_num]]))

  def plot_pixel(self):
    #use itemconfig to change the color of every canvas rectangle
    for row_num in range(1, self.data_row_size-1):                #plot every pixel in the canvas by 'for' cycle
      for column_num in range(1, self.data_column_size-1):        #plot index: 1 to data_size-2 (in 0 to data_size-1)
        self.canvas.itemconfig(self.grid_handle[row_num-1][column_num-1],
                               fill=self.color_dict[self.array_data[row_num][column_num]],
                               outline=self.color_dict[self.array_data[row_num][column_num]]) 
    self.canvas.update()    

#######################################################
#========== LITTLE FUNCRION DEFINED ===================
#######################################################

def player_guide_interface():
  print("                                                             ")
  print("                                                             ")
  print("           oooooooooo.        ooooo                 .o.      ")
  print("           888     888b.      '888'                .888.     ")
  print("           888       888b.     888                .8:888.    ")
  print("           888       8888.     888               .8' '888.   ")
  print("           888       888p.     888              .88ooo8888.  ")
  print("           888     888p.      '8888888888b     .8'     '888. ")
  print("           888888888o         o88888888888o   o88o     o8888o")
  print("                                                             ")
  print("                                                             ")
  print("               Diffusion-limited Aggregation(DLA) Model ")
  print('                         Simulation Program')
  print(' ')
  print("                   LiYang (liyang6pi5@icloud.com)")
  print("                     Last Update Date: 2018.2.27 ")
  print("                           Version: 1.0.2")
  print("                        Copyleft liyang@JPAs")
  print("                                                            ")

  while True:
    print("  ")
    print("******************************")
    print("* Set the Basic Parameter... *")
    print("******************************")
    print('Observe the Pattern of Every Step of Evolution(Y/N):')
    print(">'Y' : 'Yes, enable the step by step observation, please!'")
    print(">'N' : 'No, thanks.'")
    observe_every_evolution = raw_input('>>> ')
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
      observe_every_evolution = False

    print('  ')
    print('Use periodic boundary condition or not?(Y/N)')
    enable_periodic_map = raw_input('>>> ') 
    if ('Y' == enable_periodic_map) or ('y' == enable_periodic_map):
      enable_periodic_map = True
    else:
      enable_periodic_map = False
    
    ###set the default parameter
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

    print('   ')
    print(' DEFAULT PARAMETER LIST:')
    print('|---------------------------------')
    print('| Kernel Number:            %d' % kernel_num)
    print('| 2D Data Array Length:     %d' % dla_data_length)
    print('| 2D Data Array Width:      %d' % dla_data_width)
    print('|---------------------------------') 
    print('Change the DEFAULT parameter?(Y/N)')
    change_defult_parameter = raw_input('>>> ')
    
    if ('Y' == change_defult_parameter) or  ('y' == change_defult_parameter):
      print('Please input the Kernel Number:')
      kernel_num = input('>>> ') 
      print('Please input the 2D Data Array Length:')
      dla_data_length = input('>>> ')
      print('Please input the 2D Data Array Width:')
      dla_data_width = input('>>> ')

    print("  ")
    print("*******************************")
    print("* Basic Parameter Checking!!! *")
    print("*******************************")
    print(' BASIC PARAMETER LIST:')
    print('|---------------------------------')
    print('| Observe Every Evolution:  %s' % observe_every_evolution)
    print('| Kernel Number:            %d' % kernel_num)
    print('| 2D Data Array Length:     %d' % dla_data_length)
    print('| 2D Data Array Width:      %d' % dla_data_width)
    print('| Use Periodic Lattice:     %s' % enable_periodic_map)
    print('|---------------------------------') 
    print(' ')
    print("[  @_@  ]Start the evolution?(Y/N)")
    print("[\(>_<)/]>'Y' : 'Yeah, let's roll!'")
    print("[(¯^¯ ) ]>'N' : 'No, I’d like to reset some parameters...'")
    print(' ')

    reset_parameter = raw_input('>>> ')
    if ('N' == reset_parameter) or ('n' == reset_parameter):
      pass
    else:
      if observe_every_evolution:
        print('The new observe window has been create!!!')
      break

  print('  ')
  print("******************************")
  print("* Caluculation Processing... *")
  print("******************************")
    
  return kernel_num, dla_data_length, dla_data_width, observe_every_evolution, enable_periodic_map


def print_processing_bar(finished_count, all_count):
  ###print the processing bar of the calculation
  kProcessBarLength = 50
  process_percent = int(float(finished_count) / all_count * 1000)/10.0
  process_bar_num = int(kProcessBarLength * process_percent / 100)
  process_bar = '#' * process_bar_num + ' ' * (kProcessBarLength - process_bar_num)

  process_print = '[' + process_bar + ']' + str(finished_count) +'/' + str(all_count) +\
                  ' ====>> ' + str(process_percent) + '%'
  delete_print = '\b' * len(process_print)

  sys.stdout.write(process_print)
  sys.stdout.flush()
  sys.stdout.write(delete_print)

  return process_print


def dla_data_saved(kernel_num, dla_data_length, dla_data_width, enable_periodic_map):
  if enable_periodic_map:
    filename_arraydata = str(dla_data_length)+'X'+str(dla_data_width)+\
                         '-'+str(kernel_num)+'[peridoic].dlaarray'
    filename_plotdata = str(dla_data_length)+'X'+str(dla_data_width)+\
                         '-'+str(kernel_num)+'[peridoic].dlaplot'
  else:
    filename_arraydata = str(dla_data_length)+'X'+str(dla_data_width)+\
                         '-'+str(kernel_num)+'[aperiodic].dlaarray'
    filename_plotdata = str(dla_data_length)+'X'+str(dla_data_width)+\
                        '-'+str(kernel_num)+'[aperiodic].dlaplot'

  np.savetxt(filename_arraydata, dla_data.map, fmt="%d")
  print('  ')
  print("***************************")
  print("****   Data Saving...  ****")
  print("***************************")
  print("'xxx.dlaarray' data file created successfully!")
  print('>This data file record the fianl 2D data array of DLA.')
  print('             ')
  np.savetxt(filename_plotdata, final_position_data_sum, fmt="%d")
  print("'xxx.dlaplot' data file created successfully!")
  print('>You could use this data file to plot tha pattern of DLA ')
  print('>by using other plot software, such as GNUPLOT.')
  print('               ')
  print(' DATA FILE LIST:')
  print('|--------------------------------------------------------')
  print('| Array Data File Name:         %s' % filename_arraydata)
  print('| Coordinate Data File Name:    %s' % filename_plotdata)
  print('|--------------------------------------------------------')
  print('>>>Data Saved!!!<<<')


def program_complete():
  print('  ')
  print('>>>Program Complete!<<<')
  print('Quitting...')

#######################################################
#==================== MAIN CODE =======================
#######################################################
if __name__ == '__main__':
  #****Start the Player Guide Interface****
  kernel_num, dla_data_length, dla_data_width, \
  observe_every_evolution, enable_periodic_map  = player_guide_interface()
  
  #****DLA Data Part Set ****
  init_nuclei_array = np.array(((dla_data_width/2 - 1, dla_data_length/2 - 1),))
  dla_data = DlaData(dla_data_length, dla_data_width, init_nuclei_array, enable_periodic_map)

  #****DLA Plot Part Set****
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
    process_print = print_processing_bar(step_index, kernel_num)
    
    while not dla_data.is_stick_to_nuclei():
      dla_data.random_move_free_kernel()
      # step by step observation switch II
      if observe_every_evolution:
        dla_plot.plot_pixel()

    # save the point coordinate of the final pattern
    final_position_data_sum[step_index-1,:] = dla_data.free_kernel 
  
  print(process_print+'         ')
  print(">>>Calculation Complete!!!<<<")

  #****Output the Final Pattern****
  if not observe_every_evolution:    
    print('     ')
    print("***************************")
    print("**** Pattern Output... ****")
    print("***************************")
    print('Final Pattern is creating...')
    dla_plot.plot_pixel()
    print('>>>Final Pattern is create!!!<<<')
  
  #****Tkinter Mainloop****
  dla_plot.canvas.mainloop()     

  #****Data Save****
  dla_data_saved(kernel_num, dla_data_length, dla_data_width, enable_periodic_map)
  
  #****Quit Program****
  program_complete()


#----------------------------------------------#
###########  PROGRAM HISTORY LOG  ##############
#----------------------------------------------#
#2018.2.25 Program Strat coding
#2018.2.26 Version 1.0.0 EXPRESS
#2018.2.27 ADD: the periodic map 
#          ADD: the multiple initial nuclei
#
