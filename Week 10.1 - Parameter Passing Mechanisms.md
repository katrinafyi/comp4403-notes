# Week 10.1 &mdash; Parameter Passing Mechanisms

**Formal parameters** are the parameters used in the declaration of the procedure in its header.  The **actual parameters** are the parameters actually passed to a procedure during a call. Formal parameter names are used to access the actual parameters while in a procedure body.

For call-by-value parameters, the actual parameters are evaluated and, if necessary, coerced to the type of the formal parameter.

The values of the actual parameters are loaded onto the stack before the new stack frame is set up. Then, the formal parameters can be accessed just like local variables but with negative offsets.

_Example:_ 

```pascal
procedure fact(n: int): int =
	begin
	if n = 0 then
		return 1
    else
    	return n*fact(n-1)
   	end;
begin
	write fact(2)
end
```

A function returns a **result** and that result can be used as part of a larger expression. In the stack machine, the result is left on top of the stack after removing all call information. For this reason, space for the result is allocated before the parameters, stack frame, and everything else.

There are a number of parameter passing mechanisms:

- **Call by const** is the same as call by value but the formal parameter is a _read only_ local variable.
- **Call by value**, as discussed earlier. Assigning to the formal parameter does not change the actual parameter.
- **Call by result** is where a formal parameter acts as a local variable whose final value is assigned to the actual parameter variable. Here, the actual parameter must be an LValue of some type.
- **Call by value-result** where a single parameter acts as both a value and result parameter (as discussed above). Think MATLAB. 
- **Call by reference** the formal parameter is actually an address of the actual parameter; all references to the formal parameter affect the actual parameter (immediately). This can be done in C by passing a pointer then interacting via *.
- **Call by sharing** is just call by value but the value is a reference to an object rather than the object itself. This sounds like Java.
- **Call by name** is where the actual parameter expression is evaluated every time the formal parameter is accessed (this sounds like a bad idea).

More generally, we can pass and return procedures/functions.

- Passing procedures pass the the address of the procedure as well as the static link for the procedure's environment, i.e. the static link to be used when calling the procedure.
- Returning procedures is a little more complicated. We return the address as well as the static link for the procedure's environment. This can complicate things because the static link needs to remain valid, so the stack-based allocation of frames is no longer sufficient. Think functional programming and lambdas in Java.

In the matrix multiplication example, call by value/result works as expected but call by reference can go astray.

Variable aliasing can occur:

- Parameter aliasing in languages with call by reference is when the same variable is passed to multiple parameters; two formal parameter names for the same actual parameter variable.
- Global variable aliasing is if a global variable passed as a reference parameter. 

Pointer aliasing:

- Parameter aliasing in languages with call by sharing (like Java) is where two parameters are aliases for the same reference, called pointer aliasing.
- Similarly for global variable aliasing.

## Examples of parameters

Here are some examples of each parameter passing type, in C-style syntax as best as possible. 

Below, we try to call a function `function` with an integer parameter `param` using the different parameter passing mechanisms. Anything starting with `_` would be hidden from the programmer (but is necessary in C).

```c
// placeholder variable we can pass a reference
int param = 13; 

// call by const: param is a read only local variable
void function(const int x);
function(10);

// call by value: param is ordinary local variable
void function(int x);
function(10);

// call by result: inside function, param is a local variable.
// after function, local variable is stored in actual param.
void function(int* _result) {
    int x; 
    // do some things to set x.
    *_result = x;
}
function(&param);

// call by value-result: param is both a value and result
void function(int* _valueResult) {
    int x = *_valueResult; // get initial param value
    // do some things to compute x
    *_valueResult = x; // store result in param
}
function(&param);

// call by reference: actual param *is* the function's param
void function(ref int x) {
    x = 11; // directly changes param outside function
}
function(&&param); // somehow magically passes "param" in

// call by sharing: param is a reference, passed as value
void function(int* x) {
    *x = *x + 1;   // we can follow the reference to get/set param.
    x = something; // we can overwrite the value without changing param.
}
function(&param);

// call by name: param expression is evaluated every use
#define function(x) ((x) + (x))
function(param + 1);
// macro expands to ((param + 1) + (param + 1))
```





