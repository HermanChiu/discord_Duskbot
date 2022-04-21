import discord
import cv2 as cv
import pytesseract as tess
import numpy as np
import time
import datetime
import os
import io

from discord.ext import commands, tasks

class Ocr(commands.Cog):

  def __init__(self, bot):
    self.bot = bot