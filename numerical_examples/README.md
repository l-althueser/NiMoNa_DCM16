# Numerische Beispiele
Hier finden sich alle Implementierungen von numerischen Verfahren, die zu Testzwecken oder zur späteren Verwendung bereits erstellt wurden.

---

## Euler-Verfahren
#### Zugehörige Dateien:
* [Euler_1O.py](Euler_1O.py)  
* [Euler_1O_test.py](Euler_1O_test.py)  

#### Benutzung:
**Mittels Testscript:**  
```
python Euler_1O_test.py
```

**Im eigenem Programm:**  
```python
Euler_1O(lambda x: math.cos(x), 0, 1, 1, 1000)
```

---

## Runge-Kutta-Verfahren
### 4. Ordnung (RK4)
#### Zugehörige Dateien:
* [RK4.py](RK4.py)  
* [RKtest.py](RKtest.py)  

#### Benutzung:
**Mittels Testscript:**  
```
python RKtest.py
```

**Im eigenem Programm:**  
```python
def f(x):       #Gibt die Zeitableitung x_dot wider 
  x_dot=x       #So muss x(t)=exp(t) herauskommen 
  return x_dot 

z=RK4_method(f,z_0,dt,t0,T) 
```

---

## Dynamic Causal Modelling
### Bilineares Modell
#### Zugehörige Dateien:
* [RK4.py](RK4.py)  
* [bilinearModel.py](bilinearModel.py)  

#### Benutzung:
```
python bilinearModel.py
```

### Hermodynamisches Modell
#### Zugehörige Dateien:
* [RK4.py](RK4.py)  
* [hermodynamischesModel.py](hermodynamischesModel.py)  

#### Benutzung:
```
python hermodynamischesModel.py
```

---

## Weiterführende Informationen:
* Wikipedia: Euler Methode [Englisch](https://en.wikipedia.org/wiki/Euler_method)/[Deutsch](https://de.wikipedia.org/wiki/Explizites_Euler-Verfahren)
* [Wikipedia: Runge-Kutta Methoden](http://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods)
* [Einführung in *ordinary differential equations*](http://pauli.uni-muenster.de/tp/fileadmin/lehre/NumMethoden/WS1011/script1011ODE.pdf)
