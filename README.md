# Introduction

This is a simple Scheme interpreter that can parse and execute Scheme code. The interpreter is written in Python and uses a context-free grammar to parse the input code.

## Supported Syntax

Below is a list of all the keywords and functions that are supported by this interpreter.

Note that `val` means "any IValue", and `vals...` either means zero-or-more or one-or-more.

### Keyword Syntax

* `define` : This is a special form that binds a symbol to a value. It is used to define variables and functions.

* `if` : This is a special form that evaluates a condition. If the condition is #t, it evaluates its first argument; otherwise, it evaluates its second argument.

* `cond` : This is a special form that evaluates a series of clauses. Each clause consists of a predicate and a body. If the predicate is #t, the body is evaluated; otherwise, the next clause is evaluated.

* `lambda` : This is a special form that defines a function. It takes a list of formal parameters and a body, and returns a function object that can be called with actual arguments.

* `set!` : This is a special form that modifies the value of a variable. It takes a symbol and a value as arguments, and sets the value of the symbol to the given value.

* `begin` : This is a special form that evaluates its arguments in order. It is used to group expressions together.

* `quote` : This is a special form that returns its argument unchanged. It is used to create literal values, such as lists and vectors.

* `and` : This is a special form that evaluates its arguments from left to right. It returns #t if all arguments are non-#f values, otherwise it returns #f.

* `or` : This is a special form that evaluates its arguments from left to right. It returns the first non-#f value it encounters, or #f if all arguments are #f.

### Vector Functions

* `(vector-length vec)`
* `(vector-get vec idx)`
* `(vector-set! vec idx val)`
* `(vector vals...)` (zero or more values)
* `(vector? val)`
* `(make-vector size)`

### List Functions

* `(car cons-cell)`
* `(cdr cons-cell)`
* `(cons val1 val2)`
* `(list vals...)` (zero or more values)
* `(list? val)`
* `(set-car! cons val)`
* `(set-cdr! cons val)`

### String Functions

* `(string-append str str)`
* `(string-length str)`
* `(substring str fromInc toExc)` (fromInc and toExc are integers; first is inclusive, second is exclusive)
* `(string? val)`
* `(string-ref str int)`
* `(string-equal? str str)`
* `(string chars...)` (zero or more characters)

### Math Functions

* `(+ number...)` (one or more values)
* `(- number...)` (one or more values)
* `(* number...)` (one or more values)
* `(/ number...)` (one or more values)
* `(% number...)` (one or more values)
* `(== number...)` (one or more values)
* `(> number...)` (one or more values)
* `(>= number...)` (one or more values)
* `(< number...)` (one or more values)
* `(<= number...)` (one or more values)
* `(abs number)`
* `(sqrt number)`
* `(acos number)`
* `(asin number)`
* `(atan number)`
* `(cos number)`
* `(cosh number)`
* `(sin number)`
* `(sinh number)`
* `(tan number)`
* `(tanh number)`
* `(integer? number)`
* `(double? number)`
* `(number? number)`
* `(symbol? number)`
* `(procedure? number)`
* `(log10 number)`
* `(loge number)`
* `(pow baseNum expNum)`
* `(not val)`
* `(integer->double int)`
* `(double->integer double)`
* `(null?)`
* `(and vals...)` (one or more values)
* `(or vals...)` (one or more values)

### Math Constants

* `pi`
* `e`
* `tau`
* `inf+`
* `inf-`
* `nan`

### Fixes/Improvements Needed
* printing lists causes every element to be printed on its own line
* this interpreter is case sensitive.