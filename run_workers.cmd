if %1%==1 goto worker1
if %1%==2 goto worker2
if %1%==3 goto worker3
if %1%==4 goto worker4
if %1%==5 goto worker5
if %1%==6 goto worker6
if %1%==7 goto worker7
if %1%==8 goto worker8
if %1%==9 goto worker9
if %1%==10 goto worker10

:worker1
    start cmd /c python worker.py
    goto finished
:worker2
    start cmd /c python worker.py
    start cmd /c python worker.py
    goto finished
    
:worker3
    start cmd /c python worker.py
    start cmd /c python worker.py
    start cmd /c python worker.py
    goto finished
    
:worker4
    start cmd /c python worker.py
    start cmd /c python worker.py
    start cmd /c python worker.py
    start cmd /c python worker.py
    goto finished
    
:worker5
    start cmd /c python worker.py
    start cmd /c python worker.py
    start cmd /c python worker.py
    start cmd /c python worker.py
    start cmd /c python worker.py
    goto finished
    
:worker6
    start cmd /c python worker.py
    start cmd /c python worker.py
    start cmd /c python worker.py
    start cmd /c python worker.py
    start cmd /c python worker.py
    start cmd /c python worker.py
    goto finished
    
:worker7
    start cmd /c python worker.py
    start cmd /c python worker.py
    start cmd /c python worker.py
    start cmd /c python worker.py
    start cmd /c python worker.py
    start cmd /c python worker.py
    start cmd /c python worker.py
    goto finished
    
:worker8
    start cmd /c python worker.py
    start cmd /c python worker.py
    start cmd /c python worker.py
    start cmd /c python worker.py
    start cmd /c python worker.py
    start cmd /c python worker.py
    start cmd /c python worker.py
    start cmd /c python worker.py
    goto finished
    
:worker9
    start cmd /c python worker.py
    start cmd /c python worker.py
    start cmd /c python worker.py
    start cmd /c python worker.py
    start cmd /c python worker.py
    start cmd /c python worker.py
    start cmd /c python worker.py
    start cmd /c python worker.py
    start cmd /c python worker.py
    goto finished
    
:worker10
    start cmd /c python worker.py
    start cmd /c python worker.py
    start cmd /c python worker.py
    start cmd /c python worker.py
    start cmd /c python worker.py
    start cmd /c python worker.py
    start cmd /c python worker.py
    start cmd /c python worker.py
    start cmd /c python worker.py
    start cmd /c python worker.py
    goto finished
    
:finished
