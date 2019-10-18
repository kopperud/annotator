import pygame, sys, json, time
import pygame.locals
from termcolor import colored
#import numpy as np
import random

pygame.init()
BLACK = (0,0,0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0 ,0)
WHITE = (255,255,255)

size = (400, 800)
screen = pygame.display.set_mode(size, 0)
screen.fill(WHITE)

pygame.font.init()
font = pygame.font.SysFont("Comic Sans MS", 36)
smallfont = pygame.font.SysFont("Comic Sans MS", 18)

class annotated_data:
    def __init__(self, candidates, spans, annotator, label):
        self.candidates = candidates
        self.spans = spans
        self.annotator = annotator
        self.label = label
        self.go_next = False
    
    def __repr__(self):
        return(self.candidates)

    def go_next_toggle(self):
        self.go_next = not self.go_next

    def colored_candidate(self, i):
        candidate = self.candidates[i]
        idx = [candidate[span]["idx"] for span in self.spans]
        colors = ["cyan", "red"]

        c = []
        for i, token in enumerate(candidate["sentence"]):
            word = None          
            for ix, color in zip(idx, colors):
                if i in ix:
                    word = colored(token, color)
            if not word:
                word = token

            c.append(word)
        res = ' '.join(c)
        d = {"-LRB-": "(", "-RRB-": ")", "-LSB-": "[", "-RSB-": "]", " ,": ",", " .": ".", "( ": "(", " )": ")", " :": ":", " ;": ";"}
        for key, val in d.items():
            res = res.replace(key, val)
        return(res)

    def show_status(self, i, screen, delay = False):
        if i < 0:
            print("Error, index at minimum. Can't decrement")
            i = 0

        if i >= len(data.candidates):
            i = len(data.candidates)-1
            print("Error, index at maximum. Can't increment.")

        print("")
        print(self.colored_candidate(i))

        if delay:
            time.sleep(0.2)

        n_labelled = len([x for x in self.candidates if self.label in x.keys()])
        candidate = self.candidates[i]

        screen.fill(WHITE)
        
        y = 10
        screen.blit(font.render("Status:", True, BLACK), (10, y)); y += 40
        screen.blit(font.render("Annotator:" + self.annotator, True, BLACK), (10, y)); y += 40
        screen.blit(font.render("Index: " + str(i), True, BLACK), (10, y)); y += 40

        if self.label in candidate.keys():
            label = str(candidate[self.label])
        else:
            label = "not assigned"

        screen.blit(font.render("Label: " + label, True, BLACK), (10, y)); y += 90
        screen.blit(font.render("Candidate annotator. Menu:", True, BLACK), (10, y)); y += 40
        screen.blit(smallfont.render("LEFT: go to previous", True, BLACK), (10, y)); y += 20
        screen.blit(smallfont.render("RIGHT: go to next", True, BLACK), (10, y)); y += 20
        screen.blit(smallfont.render("p: print status", True, BLACK), (10, y)); y += 20
        screen.blit(smallfont.render("t: assign TRUE", True, BLACK), (10, y)); y += 20
        screen.blit(smallfont.render("f: assign FALSE", True, BLACK), (10, y)); y += 20

        if self.go_next:
            capt = "(yes)"
        else:
            capt = "(no)"
        screen.blit(smallfont.render(f"x: go next after assign? {capt}", True, BLACK), (10, y)); y += 20
        screen.blit(smallfont.render("g: go to next unlabelled", True, BLACK), (10, y)); y += 20
        screen.blit(smallfont.render("s: save", True, BLACK), (10, y)); y += 20
        screen.blit(smallfont.render("ESC: exit (no save)", True, BLACK), (10, y)); y += 40

        screen.blit(font.render("Information:", True, BLACK), (10, y)); y += 40
        screen.blit(smallfont.render(f"Label: \"{label}\"", True, BLACK), (10, y)); y += 20
        spans_str = '\", \"'.join(spans)
        screen.blit(smallfont.render(f"Spans: \"{spans_str}\"", True, BLACK), (10, y)); y += 20
        screen.blit(smallfont.render(f"n = {len(candidates)}", True, BLACK), (10, y)); y += 20

        screen.blit(smallfont.render(f"n_labelled = {n_labelled}", True, BLACK), (10, y))

        


i = 0
annotator = "btk"

if True:
    spans = ["TAXA", "LOCATION"]
    label = "label"

else:
    spans = ["LOCATION"]
    label = "toponym_label"

#fpath = "data/candidates_annotated.json"
#fpath = "data/annotated2.json"
#fpath = "data/annotated3.json"
fpath = "data/candidates_correct_toponym.json"
#n_sample = 1000


with open(fpath, "r") as f:
    candidates = json.loads(f.read())

data = annotated_data(candidates, spans, annotator, label)


while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p: # replace the 'p' to whatever key you wanted to be pressed
             #   print(data.colored_candidate(i))
                data.show_status(i, screen)

            if event.key == pygame.K_LEFT:
                i -= 1
                data.show_status(i, screen)
            if event.key == pygame.K_RIGHT:
                i += 1
                data.show_status(i, screen)

            if event.key == pygame.K_t:
                data.candidates[i][label] = True
#                data.show_status(i, screen)
                screen.blit(font.render("Assigned True", True, BLACK), (10, 200))

                if data.go_next:
                    i += 1                
                    data.show_status(i, screen, delay = True)

            if event.key == pygame.K_f:
                data.candidates[i][label] = False
#                data.show_status(i, screen)
                screen.blit(font.render("Assigned False", True, BLACK), (10, 200))

                if data.go_next:
                    i += 1
                    data.show_status(i, screen, delay = True)


            if event.key == pygame.K_g:
                unlabeled = [i for i,x in enumerate(data.candidates) if label not in x.keys()]
                if unlabeled:
                    i = unlabeled[0]
                    print(f"Set index at {i}.")
                    data.show_status(i, screen)
                else:
                    print("Can't find any unlabeled")

            if event.key == pygame.K_l:
                labeled = [j for j,x in enumerate(data.candidates) if label in x.keys()]
                labeled = [j for j in labeled if j >= i]
                if labeled:
                    i = labeled[0]
                    print(f"Set index at {i}.")
                    data.show_status(i, screen)
                else:
                    print("Can't find any labeled candidates.")

            if event.key == pygame.K_x:
                data.go_next_toggle()
                data.show_status(i, screen)
                    
            
            if event.key == pygame.K_s:
                data.show_status(i, screen)

                with open(fpath, "w") as f:
                    f.write(json.dumps(data.candidates))

                screen.blit(font.render(f"Written to file \"{fpath}\"", True, BLACK), (10, 200))           
                print(f"Written to file \"{fpath}\"")

                
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()


    pygame.display.update()
