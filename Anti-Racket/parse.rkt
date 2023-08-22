#lang racket
(provide parse)
(require "ast.rkt")

;; S-Expr -> Expr
(define (parse s)
  (match s
    [(? exact-integer? s) (Int s)]
    [(? boolean? s) (Bool s)]
    [(? char? s)    (Char s)]    
    ['eof           (Eof)]
    [(list (? op0? o))    (Prim0 o)]
    [(list e (? op1? o))  (Prim1 o (parse e))]
    [(list e2 e1 'begin)  (Begin (parse e1) (parse e2))]
    [(list e3 e1 e2 'if)
     (If (parse e1) (parse e2) (parse e3))]
    [_ (error "Parse error")]))

;; Any -> Boolean
(define (op0? x)
  (memq x '(read-byte peek-byte)))

;; Any -> Boolean
(define (op1? x)
  (memq x '(add1 sub1 zero? char? integer->char char->integer
                 write-byte eof-object?)))
