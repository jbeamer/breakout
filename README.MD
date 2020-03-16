
# breakout

__BirksBeamer Breakout__

This is a simple version of the classic game Breakout, written using the PyGame library.
I have been using it to teach my kids to program, and they have their own versions.
***


## Point
```python
Point(self, x, y)
```
a simple class to keep track of coordinates

## BreakoutPaddle
```python
BreakoutPaddle(self)
```
' BreakoutPaddle class

### set_location
```python
BreakoutPaddle.set_location(x)
```
moves the paddle to the provided location

### move
```python
BreakoutPaddle.move(relative_x)
```
move the paddle by a relative amount from current location

## BreakoutBrick
```python
BreakoutBrick(self, col, row, power_up=False)
```
' BreakoutBrick class

### screen_loc
```python
BreakoutBrick.screen_loc()
```
screen_loc is a simple helper to get the brick's drawn location

## BreakoutBall
```python
BreakoutBall(self)
```
' BreakoutBall class

### set_location
```python
BreakoutBall.set_location(x, y, vel_x, vel_y)
```
moves the ball to the provided location

### hit
```python
BreakoutBall.hit(brick)
```
check for brick hit

### move
```python
BreakoutBall.move(paddle, bricks)
```
moves the ball, bounce off the constraints of our field, and check
for brick and paddle hits

## BreakoutGame
```python
BreakoutGame(self)
```
' BreakoutGame class

### bricks_left
```python
BreakoutGame.bricks_left()
```
bricks left: just a quick helper to count the remaining bricks

### game_loop
```python
BreakoutGame.game_loop()
```
this function is called repeatedly to handle the functioning of the game experience

### play
```python
BreakoutGame.play()
```
the main function of the BreakoutGame object, sets up a clock to
call our loop function repeatedly at 60 Hz

### draw_window
```python
BreakoutGame.draw_window(winner=False)
```
draw_window function

## main
```python
main()
```
main function
