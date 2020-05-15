"""
Reinforcement learning maze example.

Red rectangle:		  explorer.
Black rectangles:	   hells	   [reward = -1].
Yellow bin circle:	  paradise	[reward = +1].
All other states:	   ground	  [reward = 0].

This script is the environment part of this example.
The RL is in RL_brain.py.

View more on my tutorial page: https://morvanzhou.github.io/tutorials/
"""
import numpy as np
import time
import sys
import subprocess
import random
import math
if sys.version_info.major == 2:
	import Tkinter as tk
else:
	import tkinter as tk

UNIT = 10   # pixels
MAZE_H = 4  # grid height
MAZE_W = 4  # grid width
SHOW = False



Width = 15
Height = 15
BlockSize = 10
WaitTime = 50
PlayerNumber = 2
Range = 5
BlockNumber = 20
GroundBlockRate = 0.75
Play = True
Seed = int(time.time())
Game = 'link.exe'
AIs = []
Blocks = []
TimeLimit = 1
Dirs = [[-1, -1], [-1, 1], [0, -1], [-1, 0]]
Output = True

ScoreCount = 300
class Maze(tk.Tk, object):
	def __init__(self):
		super(Maze, self).__init__()
		#self.action_space = ['u', 'd', 'l', 'r']
		self.n_actions = Width
		self.n_features = Height * Width * 4
		self.title('Link')
		self.geometry('{0}x{1}'.format(Height * UNIT, Width * UNIT))
		self._build_maze()
		self.blocks = []
		self.field = [[-1 for j in range(Width)] for i in range(Height)]
		self.top = [0 for i in range(0, Width)]
		self.cell = []
		self.ai = subprocess.Popen('ai0.exe', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
		self.TotalNumber = 0
		self.RecentScoreList = [0] * ScoreCount
	
	def VaildCoord(self, x, y):
		if x<0 or x>=Height:
			return False
		if y<0 or y>=Width:
			return False
		return True
	
	def judgeValidity(self, column):
		if column<0 or column>=Width:
			return False
		row = self.top[column]
		if row>=Height:
			return False
		if (self.field[row][column]!=-1):
			return False
		
		minHeight = self.top[0]
		for i in range(1, Width):
			if minHeight>self.top[i]:
				minHeight = self.top[i]
		
		next = row + 1
		while(self.VaildCoord(next, column) and self.field[next][column]!=-1):
			next += 1
		if (next - minHeight > Range):
			return False
		
		return True
		
	def getFeature(self, color=0):
		res = []
		for i in range(Height):
			for j in range(Width):
				for k in [-2,-1,0,1]:
					if self.field[i][j] == k:
						res.append(1)
					else:
						res.append(0)
		
		return np.array(res)
		
		for i in range(0, Width):
			if (not self.judgeValidity(i)):
				res += [0,0,0,0,0,0]
				continue
			for Dir in Dirs:
				for flag in [1, -1]:
					x = self.top[i] + Dir[0]*flag
					y = i + Dir[1]*flag
					count = 1
					while (self.VaildCoord(x, y) and self.field[x][y] == color):
						count+=1
						x += Dir[0]*flag
						y += Dir[1]*flag
					res.append(count)
		return np.array(res)

	def _build_maze(self):
		if (SHOW):
			self.canvas = tk.Canvas(self, bg='black',
							   height=Height * UNIT,
							   width=Width * UNIT)

			# create grids
			for c in range(0, MAZE_W * UNIT, UNIT):
				x0, y0, x1, y1 = c, 0, c, MAZE_H * UNIT
				self.canvas.create_line(x0, y0, x1, y1)
			for r in range(0, MAZE_H * UNIT, UNIT):
				x0, y0, x1, y1 = 0, r, MAZE_W * UNIT, r
				self.canvas.create_line(x0, y0, x1, y1)
		self.blocks = []
		self.field = [[-1 for j in range(Width)] for i in range(Height)]
		self.top = [0 for i in range(0, Width)]

		#self.hell1 = self.canvas.create_rectangle(
		#	hell1_center[0] - 15, hell1_center[1] - 15,
		#	hell1_center[0] + 15, hell1_center[1] + 15,
		#	fill='black')
		# hell
		# hell2_center = origin + np.array([UNIT, UNIT * 2])
		# self.hell2 = self.canvas.create_rectangle(
		#	 hell2_center[0] - 15, hell2_center[1] - 15,
		#	 hell2_center[0] + 15, hell2_center[1] + 15,
		#	 fill='black')

		# create oval
		#oval_center = origin + UNIT * 2
		#self.oval = self.canvas.create_oval(
		#	oval_center[0] - 15, oval_center[1] - 15,
		#	oval_center[0] + 15, oval_center[1] + 15,
		#	fill='yellow')

		# create red rect
		#self.rect = self.canvas.create_rectangle(
		#	origin[0] - 15, origin[1] - 15,
		#	origin[0] + 15, origin[1] + 15,
		#	fill='red')

		# pack all
		if (SHOW):
			self.canvas.pack()
	def f(self, x):
		return x*x*x
		
	def getScore(self):
		res = [0 for i in range(PlayerNumber)]
		for i in range(Height):
			for j in range(Width):
				for dir in Dirs:
					if self.field[i][j] >= 0 and ((not self.VaildCoord(i-dir[0], j-dir[1])) or self.field[i-dir[0]][j-dir[1]]!=self.field[i][j]):
						x = i
						y = j
						count = -1
						while(self.VaildCoord(x, y) and self.field[x][y]==self.field[i][j]):
							x += dir[0]
							y += dir[1]
							count += 1
						res[self.field[i][j]] += self.f(count)
		return res
		
	def reset(self):
		self.update()
		time.sleep(0.1)
		self.blocks = []
		self.field = [[-1 for j in range(Width)] for i in range(Height)]
		for r in self.cell:
			self.canvas.delete(r)
		self.cell = []
		
		GroundBlockNumber = int(BlockNumber * GroundBlockRate)
		self.top = [0 for i in range(Width)]
		for i in range(GroundBlockNumber):
			column = random.randint(0, Width-1)
			random.seed(column + self.top[column] + Seed)
			if (self.top[column] < Height):
				self.blocks.append([self.top[column], column])
				self.top[column] += 1
			else:
				self.blocks.append([self.top[column] - 1, column])
				
		for i in range(GroundBlockNumber, BlockNumber):
			self.blocks.append([random.randint(0, Height - 1), random.randint(0, Width-1)])
			
		for block in self.blocks:
			self.field[block[0]][block[1]] = -2
			self.updateTop(block[1])
			self.addRect(block)
		
		
		self.ai.terminate()
		GameInfo = str(Height)+' '+str(Width)+' '+str(PlayerNumber)+' '+str(BlockNumber)+' '+str(Range)+'\n'	
		for block in self.blocks:
			GameInfo += str(block[0])+' '+str(block[1])+'\n'
		#print(GameInfo)
			
		self.ai = subprocess.Popen('ai0.exe', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
		self.ai.stdin.write(GameInfo.encode(encoding='utf-8'))
		self.ai.stdin.flush()
		#self.canvas.delete(self.rect)
		#origin = np.array([20, 20])
		#self.rect = self.canvas.create_rectangle(
		#	origin[0] - 15, origin[1] - 15,
		#	origin[0] + 15, origin[1] + 15,
		#	fill='red')
		# return observation
		return self.getFeature()

	def getOver(self):
		for x in self.top:
			if x < Height:
				return False
		return True
	
	def updateTop(self, column):
		while(self.VaildCoord(self.top[column], column) and self.field[self.top[column]][column] != -1):
				self.top[column] += 1
	
	def addRect(self, Coord):
		if (SHOW == False):
			return
		color = ['red', 'blue', 'grey', 'black']
		self.cell.append(self.canvas.create_rectangle(
			Coord[1]*UNIT, Coord[0]*UNIT,
			(Coord[1]+1)*UNIT, (Coord[0]+1)*UNIT,
			fill=color[self.field[Coord[0]][Coord[1]]]))
		
	def step(self, action):
		score1 = self.getScore()
		action2 = int(self.ai.stdout.readline().decode('utf-8').strip().split(' ')[0])
		#print(action2, self.judgeValidity(action2))
		debug = self.ai.stdout.readline()
		self.ai.stdin.write((str(action)+'\n').encode(encoding='utf-8'))
		self.ai.stdin.flush()
		#print(action, action2)
		
		if self.judgeValidity(action) and action == action2:
			self.field[self.top[action]][action] = -2
			self.addRect([self.top[action], action])
			self.updateTop(action)
		else:
			if self.judgeValidity(action):
				self.field[self.top[action]][action] = 0
				self.addRect([self.top[action], action])
				self.updateTop(action)
			if self.judgeValidity(action2):
				self.field[self.top[action2]][action2] = 1
				self.addRect([self.top[action2], action2])
				self.updateTop(action2)
		
		score2 = self.getScore()
		reward = (math.log(score2[0]+1) - math.log(score2[1]+1)) - (math.log(score1[0]+1) - math.log(score1[1]+1))
		if (reward < 0):
			reward = -math.exp(-reward)
		else:
			reward = math.exp(reward)
		if (self.getOver()):
			self.TotalNumber+=1
			self.RecentScoreList[self.TotalNumber%ScoreCount] = (score2[0]+1)/(score2[1]+1)
			print(score2, np.mean(self.RecentScoreList))
		return self.getFeature(), reward, self.getOver()
		
		s = self.canvas.coords(self.rect)
		base_action = np.array([0, 0])
		if action == 0:   # up
			if s[1] > UNIT:
				base_action[1] -= UNIT
		elif action == 1:   # down
			if s[1] < (MAZE_H - 1) * UNIT:
				base_action[1] += UNIT
		elif action == 2:   # right
			if s[0] < (MAZE_W - 1) * UNIT:
				base_action[0] += UNIT
		elif action == 3:   # left
			if s[0] > UNIT:
				base_action[0] -= UNIT

		self.canvas.move(self.rect, base_action[0], base_action[1])  # move agent

		next_coords = self.canvas.coords(self.rect)  # next state

		# reward function
		if next_coords == self.canvas.coords(self.oval):
			reward = 1
			done = True
		elif next_coords in [self.canvas.coords(self.hell1)]:
			reward = -1
			done = True
		else:
			reward = 0
			done = False
		s_ = (np.array(next_coords[:2]) - np.array(self.canvas.coords(self.oval)[:2]))/(MAZE_H*UNIT)
		return s_, reward, done

	def render(self):
		# time.sleep(0.01)
		if (SHOW):
			self.update()


