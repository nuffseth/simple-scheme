; Vectors
(define vec1 '#(1 2 3 4))
(vector-length vec1)    ; 4
(vector-get vec1 1)     ; 2
(vector-set! vec1 1 7)
(vector-get vec1 1)     ; 7
(vector? vec1)          ; #t

(define vec2 (vector 1 2 3))
(vector-length vec2)    ; 3
(vector-get vec2 1)     ; 2
(vector-set! vec2 1 7)
(vector-get vec2 1)     ; 7
(vector? vec2)          ; #t

(define vec2 (make-vector 6))
(vector-get vec2 1)     ; #f
(vector-set! vec2 1 7)
(vector-get vec2 1)     ; 7
(vector? vec2)          ; #t
(vector? '#())          ; #t
(vector? (make-vector 0)) ; #t
(vector? (vector))      ; #t


; Lists
(define list1 '(1 2 3 4))
(car list1)     ; 1
(cdr list1)     ; (2 3 4)
(cons -3 list1) ; (-3 1 2 3 4)
(define list2 (list 1 2 3))
list2           ; (1 2 3)
(cons 5 '())    ; (5)
(list? 5)       ; #f
(list? '())     ; #t
(list? '(1))    ; #t
(list? '(1 2))  ; #t
(list? (list))  ; #t
(list? (list 1 2)) ; #t
(set-car! list1 -8)
list1           ; (-8 2 3 4)
(set-cdr! list1 '(6))
list1           ; (-8 6)


; Strings
(define str1 "Hello, world!")
str1                        ; "Hello, world!"
(string-append str1 " foo") ; "Hello, world! foo"
(string-length str1)        ; 13
(substring str1 1 4)        ; "ell"
(string? str1)              ; #t
(string? 5)                 ; #f
(string-ref str1 4)         ; #\o
(string-equal? str1 "foo")  ; #f
(string-equal? str1 "Hello, world!") ; #t
(string #\b #\a #\r)        ; "bar"


; Math
(+ 3 5)     ; 8
(- 3 5)     ; -2
(* 3 5)     ; 15
(/ 8 4)     ; 2
(/ 2 3)     ; 0.666
(% 8 5)     ; 3
(== 8 9)    ; #f
(== 8 8)    ; #t
(== 8 3)    ; #f
(> 8 9)     ; #f
(> 8 8)     ; #f
(> 8 3)     ; #t
(>= 8 9)    ; #f
(>= 8 8)    ; #t
(>= 8 3)    ; #t
(< 8 9)     ; #t
(< 8 8)     ; #f
(< 8 3)     ; #f
(<= 8 9)    ; #t
(<= 8 8)    ; #t
(<= 8 3)    ; #f
(abs 5)     ; 5
(abs 0)     ; 0
(abs -4)    ; 4
(abs 5.8)   ; 5.8
(abs -4.6)  ; 4.6
(abs 0.0)   ; 0.0
(abs inf+)  ; inf+
(abs inf-)  ; inf+
(abs pi)    ; 3.14159
(sqrt 2)    ; 1.41...
(acos 0.8)
(asin 0.8)
(atan 0.8)
(cos 0.8)
(cosh 0.8)
(sin 0.8)
(sinh 0.8)
(tan 0.8)
(tanh 0.8)
(integer? 1.3)  ; #f
(integer? 3)    ; #t
(double? 1.3)   ; #t
(double? 3)     ; #f
(number? 5)     ; #t
(number? 5.8)   ; #t
(number? "hi")  ; #f
(symbol? 'a)    ; #t
(symbol? 3)     ; #f
(procedure? +)  ; #t
(define lambda1 (lambda (formal1) (+ formal1 1)))
(procedure? lambda1)    ; #t
(log10 1.3)
(loge 1.3)
(pow 5 3)   ; 125
(not #t)    ; #f
(not #f)    ; #t
(not 3)     ; #f
(integer? (integer->double 5))      ; #f
(double? (integer->double 5))       ; #t
(integer? (double->integer 5.8))    ; #t
(double? (double->integer 5.8))     ; #f
(null? '())     ; #t
(null? '#())    ; #f
(null? #f)      ; #f
(null? #t)      ; #f