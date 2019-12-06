#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 19:28:27 2019

@author: 3701222
"""

from hog import hog
import dice


import tkinter as tk
from tkinter import *
import argparse

class BetterWidget(object):
    """A BetterWidget returns itself on pack and config for call chaining."""
    def pack(self, **kwargs):
        super().pack(**kwargs)
        return self

    def config(self, **kwargs):
        super().config(**kwargs)
        return self

class TextWidget(BetterWidget):
    """A TextWidget contains a mutable line of text."""
    def __init__(self, **kwargs):
        self.textvar = kwargs.get('textvariable', tk.StringVar())
        self.config(textvariable=self.textvar)
        if 'text' in kwargs:
            self.textvar.set(kwargs['text'])

    @property
    def text(self):
        return self.textvar.get()

    @text.setter
    def text(self, value):
        return self.textvar.set(str(value))


class Label(TextWidget, tk.Label):
    """A Label is a text label."""
    def __init__(self, parent, **kwargs):
        kwargs.update(label_theme)
        tk.Label.__init__(self, parent, **kwargs)
        TextWidget.__init__(self, **kwargs)

class Button(BetterWidget, tk.Button):
    """A Button is an interactive button."""
    def __init__(self, *args, **kwargs):
        kwargs.update(button_theme)
        tk.Button.__init__(self, *args, **kwargs)

class Entry(TextWidget, tk.Entry):
    """An Entry widget accepts text entry."""
    def __init__(self, parent, **kwargs):
        kwargs.update(entry_theme)
        tk.Entry.__init__(self, parent, **kwargs)
        TextWidget.__init__(self, **kwargs)

class Frame(BetterWidget, tk.Frame):
    """A Frame contains other widgets."""
    def __init__(self, *args, **kwargs):
        kwargs.update(frame_theme)
        tk.Frame.__init__(self, *args, **kwargs)


def name(who):
    """Return the name of a player."""
    return "Joueur {0}".format(who)


class HogGUIException(BaseException):
    """HogGUI-specific Exception. Used to exit a game prematurely."""
    pass







class HogGUI(Frame):
    """Tkinter GUI for Hog."""
    KILL = -9

    
    
    def __init__(self, parent, computer=False):
        """Replace hog module's dice with hooks to GUI and start a game.
        parent   -- parent widget (should be root)
        computer -- True if playing against a computer
        """
        
        D = 20
        N = 100
        self.h = hog(D,N)
        
        self.STRATEGIES=[self.h.strategie_aveugle(),self.h.strategie_toujour_lancer(3)] 
        
        super().__init__(parent)
        self.pack(fill=BOTH)
        self.parent = parent
        self.who = 0

        self.init_scores()
        self.strs()
        self.init_rolls()
        self.init_dice()
        self.init_status()
        self.init_restart()

        six_sided = self.make_dice()
        self.computer, self.turn = computer, 0
        self.play()

    def init_scores(self):
        """Creates child widgets associated with scoring.
        Each player has a score Label that is updated each turn. Scores can be
        accessed and modified through Tkinter variables in self.score_vars.
        """
        self.score_frame = Frame(self).pack()

        self.p_frames = [None, None]
        self.p_labels = [None, None]
        self.s_labels = [None, None]
        for i in (0, 1):
            self.p_frames[i] = Frame(self.score_frame, padx=25).pack(side=LEFT)
            self.p_labels[i] = Label(self.p_frames[i],
                        text=name(i) + ':').pack()
            self.s_labels[i] = Label(self.p_frames[i]).pack()



    def init_rolls(self):
        """Creates child widgets associated with the number of rolls.
        The primary widget is an Entry that accepts user input. An intermediate
        Tkinter variable, self.roll_verified, is set to the final number of
        rolls. Once it is updated, the player immediately takes a turn based on
        its value.
        """
        self.roll_frame = Frame(self).pack()

        self.roll_label = Label(self.roll_frame).pack()
        self.roll_entry = Entry(self.roll_frame,justify=CENTER).pack()
        self.roll_entry.bind('<Return>',lambda event: self.roll_button.invoke())
        self.roll_verified = IntVar()
        self.roll_button = Button(self.roll_frame,text='Lancer!', command=self.roll).pack()

    def strs(self):
        """Creates child widgets associated with the number of rolls.
        The primary widget is an Entry that accepts user input. An intermediate
        Tkinter variable, self.roll_verified, is set to the final number of
        rolls. Once it is updated, the player immediately takes a turn based on
        its value.
        """
        self.myStrategy = self.h.strategie_optimale()
        self.strategy_changed = False

        def random():
                self.strategy_changed = True
                self.myStrategy = self.h.strategie_aleatoire()
                self.active_strategy.text ="Strategie active: Random"
                
        def optimal():
                self.strategy_changed = True
                self.myStrategy = self.h.strategie_optimale()
                self.active_strategy.text ="Strategie active: Optimal"
        def aveugle():
                self.strategy_changed = True
                self.myStrategy = self.h.strategie_aveugle()
                self.active_strategy.text ="Strategie active: Aveugle"
                
        self.st = Frame(self)
        self.st.pack(fill=BOTH, expand=True)
        self.active_strategy = Label(self.st).pack()   
        self.aveugle = Button(self.st,text='Aveugle', command=aveugle)
        self.aveugle.pack(side=LEFT) 
        self.Optimal = Button(self.st,text='Optimal', command=optimal)
        self.Optimal.pack(side=LEFT)
        self.Random  = Button(self.st,text='Random', command=random)
        self.Random.pack(side=LEFT)
        
        
        
    def init_dice(self):
        """Creates child widgets associated with dice. Each dice is stored in a
        Label. Dice Labels will be packed or unpacked depending on how many dice
        are rolled.
        """
        self.dice_frames = [
            Frame(self).pack(),
            Frame(self).pack()
        ]
        self.dice = {
            i: Label(self.dice_frames[i//5]).
                    config(image=HogGUI.IMAGES[6]).
                    pack(side=LEFT)
            for i in range(10)
        }

    def init_status(self):
        """Creates child widgets associated with the game status. For example,
        Hog Wild is displayed here."""
        self.status_label = Label(self).pack()


    def init_restart(self):
        """Creates child widgets associated with restarting the game."""
        self.restart_button = Button(self, text='Restart',
                                     command=self.restart).pack()


    def make_dice(self):
        """Creates a dice function that hooks to the GUI and wraps
        dice.make_fair_dice.
        sides -- number of sides for the die
        """
        fair_dice = dice.dice()
        def gui_dice():
            """Roll fair_dice and add a corresponding image to self.dice."""
            result = fair_dice()
            img = HogGUI.IMAGES[result]
            self.dice[self.dice_count].config(image=img).pack(side=LEFT)
            self.dice_count += 1
            return result
        return gui_dice

    def clear_dice(self):
        """Unpacks (hides) all dice Labels."""
        for i in range(10):
            self.dice[i].pack_forget()


    def roll(self):
        """Verify and set the number of rolls based on user input. As
        per game rules, a valid number of rolls must be an integer
        greater than or equal to 0.
        """
        result = self.roll_entry.text
        if result.isnumeric() and 10 >= int(result) >= 0:
            self.roll_verified.set(int(result))





    def switch(self, who=None):
        """Switches players. self.who is either 0 or 1."""
        self.p_frames[self.who].config(bg=bg)
        self.p_labels[self.who].config(bg=bg)
        self.s_labels[self.who].config(bg=bg)
        self.who = 1 - self.who if who is None else who
        self.p_frames[self.who].config(bg=select_bg)
        self.p_labels[self.who].config(bg=select_bg)
        self.s_labels[self.who].config(bg=select_bg)


    def restart(self):
        """Kills the current game and begins another game."""
        self.roll_verified.set(HogGUI.KILL)
        self.status_label.text = ''
        self.clear_dice()
        self.play()

    def destroy(self):
        """Overrides the destroy method to end the current game."""
        self.roll_verified.set(HogGUI.KILL)
        super().destroy()






    def play(self):
        """Simulates a game of Hog by calling hog.play with the GUI strategies.
        If the player destroys the window prematurely (i.e. in the
        middle of a game), a HogGUIException is raised to exit out
        of play's loop. Otherwise, the widget will be destroyed,
        but the strategy will continue waiting.
        """
        self.turn = 1 - self.turn
        self.switch(0)
        self.s_labels[0].text = '0'
        self.s_labels[1].text = '0'
        self.status_label.text = ''
        try:
            score, score_adverse = self.h.jouer(self.strategy, self.strategy)
        except HogGUIException:
            pass
        else:
            self.s_labels[0].text = score
            self.s_labels[1].text = score_adverse
            winner = 0 if score > score_adverse else 1
            self.status_label.text = 'Game over! {} GAGNE ^_^ !'.format(name(winner))





    def strategy(self,score,score_adverse):

        s0 = score if self.who == 0 else score_adverse
        s1 = score_adverse if self.who == 0 else score

        self.s_labels[0].text = s0
        self.s_labels[1].text = s1

        self.roll_label.text = name(self.who) +' va jouer:'

        status = self.status_label.text

        if self.computer and self.who == self.turn:
            self.update()
            self.after(DELAY)
            
            self.Random.config(state="disabled")
            self.Optimal.config(state="disabled")
            self.aveugle.config(state="disabled")
            
            
            if(not self.strategy_changed ):
                self.active_strategy.text ="Strategie active: Optimal"
                
            result = self.myStrategy(score,score_adverse)
        else:
            self.roll_entry.focus_set()
            self.wait_variable(self.roll_verified)
            result = self.roll_verified.get()
            self.roll_entry.text = ''
        if result == HogGUI.KILL:
            raise HogGUIException

        self.clear_dice()
        self.dice_count = 0
        self.status_label.text = '{} a choisi de lancer {}.'.format(name(self.who),result)
        self.switch()
        return result



def run_GUI(computer=False):
    """Start the GUI.
    computer -- True if playing against computer
    """
    root = Tk() #Toplevel()
    root.title('Dice Battles')
    root.minsize(800, 470)
    root.geometry("520x400")

    # Tkinter only works with GIFs
    HogGUI.IMAGES = {
        1: PhotoImage(file='./images/die1.gif'),
        2: PhotoImage(file='./images/die2.gif'),
        3: PhotoImage(file='./images/die3.gif'),
        4: PhotoImage(file='./images/die4.gif'),
        5: PhotoImage(file='./images/die5.gif'),
        6: PhotoImage(file='./images/die6.gif'),
    }

    app = HogGUI(root, computer)
    root.mainloop()


select_bg = '#a6d785'
bg='#ffffff'
fg='#000000'
font=('Arial', 14)

frame_theme = {
    'bg': bg,
}

label_theme = {
    'font': font,
    'bg': bg,
    'fg': fg,
}

button_theme = {
    'font': font,
    'activebackground': select_bg,
    'bg': bg,
    'fg': fg,
}

entry_theme = {
    'fg': fg,
    'bg': bg,
    'font': font,
    'insertbackground': fg,
}


DELAY=2000

def run(ifComputer):
    run_GUI(computer=ifComputer)