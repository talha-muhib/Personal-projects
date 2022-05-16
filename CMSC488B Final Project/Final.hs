{-# LANGUAGE FlexibleContexts #-}
{-# LANGUAGE TemplateHaskell #-}
{-# LANGUAGE ScopedTypeVariables #-}

module Final where
import Test.QuickCheck
import Test.HUnit
import Data.Array
import Data.List
import Control.Monad (liftM2, liftM3)

{-
Name: Talha Muhib
Class: CMSC488B - Advanced Functional Programming
Final Project: Dynamic Programming in Haskell

We will look at several different DP problems, starting with the classic Fibonacci, 
then move on to other more complicated problems such as. I was told I should do minimum 3 problems so:

Longest subsequence
Buy low, sell high
Rod cutting
Edit string distancing (I'm sort of cheating with this because I found it in the slides but I mainly used the code as a guide)
-}

fib :: Int -> Int
fib n
    | n <= 1 = 1
    | otherwise = (fib $ n - 1) + (fib $ n - 2)

{-
Pretty straightforward. Only problem is this algorithm runs in exponential time 2^n.

A cool little thing is that because of Haskell's lazy evaluation,
it is able to use "infinite data structures." 
Let's rewrite the fib function this way now:
-}

fib_dp :: Int -> Int
fib_dp n
    | n <= 1 = 1
    | otherwise = let lst2 = take (n - 1) (infinite_list 1) in
        let fib_lst = foldl (\a h -> let i = (a !! 0) + (a !! 1) in i : a) [1, 1] lst2 in
            head fib_lst

{- 
This new implementation takes polynomial time instead of 2^n, a massive improvement.
There is also another way to do this using the Array type:
-}

fib_dp2 :: Int -> Int
fib_dp2 n = 
    let bounds = (0, n) in
    let fib_lst = listArray bounds [fib_dp i | i <- range bounds] in
        fib_lst ! n

-- Testing fib properties: results for both implementations should be the same
tfib :: Test
tfib = "fib" ~: TestList[
    (fib 10) ~?= (fib_dp 10),
    (fib 15) ~?= (fib_dp 15),
    (fib 20) ~?= (fib_dp 20),
    (fib 25) ~?= (fib_dp 25),
    (fib 30) ~?= (fib_dp 30),
    (fib 32) ~?= (fib_dp 32)]

-- Adding a quickCheck for fib
prop_fib :: Property
prop_fib = forAll (genInt 27) (\i -> fib i == fib_dp i && fib_dp i == fib_dp2 i)


-- Now we can apply this to a few more problems:
-- 1) Longest subsequence
subseq :: [Int] -> Int
subseq [] = 0
subseq l = let max_end = 1 in let n = length l - 1 in subseq_aux l 0 n max_end

subseq_aux :: [Int] -> Int -> Int -> Int -> Int
subseq_aux l i n max_end 
    | i > n = max_end
    | otherwise = let new_max = (max max_end (traverse' l i)) in subseq_aux l (i + 1) n new_max

traverse' :: [Int] -> Int -> Int
traverse' _ 0 = 1
traverse' l n = let max_end = 1 in traverse_aux l 0 n max_end

traverse_aux :: [Int] -> Int -> Int -> Int -> Int
traverse_aux l i n max_end 
    | i > n = max_end
    | otherwise = let bt = (traverse' l i) in 
                  let m2 = if l !! i < l !! n then max (bt + 1) max_end else max_end in traverse_aux l (i + 1) n m2

{- 
At every step of this algorithm we are asking "is this number part of the longest sequence? Yes or no?"
If there are n numbers this would take 2^n choices, which is just as bad as the naive fibonacci algorithm.
Let's see how we do this using dp. There are a few ways we can do this. Here's one way:
-}

subseq_dp :: [Int] -> Int
subseq_dp l = subseq_dp_aux l []

subseq_dp_aux :: [Int] -> [Int] -> Int
subseq_dp_aux [] l = length l
subseq_dp_aux (h : t) l = let new_l = inserts l h in subseq_dp_aux t new_l

inserts :: [Int] -> Int -> [Int]
inserts [] n = [n]
inserts (h : t) n = if n > h then h : (inserts t n) else (n : t)

-- Here's another way using Arrays:
subseq_dp2 :: [Int] -> Int
subseq_dp2 l = 
    let bounds = (0, length l - 1) in
    let array = listArray bounds [i | i <- l] in
        subseq_dp2_aux array 0 (length l) []

subseq_dp2_aux :: Array Int Int -> Int -> Int-> [Int] -> Int
subseq_dp2_aux  arr i n l 
    | i >= n = length l 
    | otherwise = let new_l = inserts l (arr ! i) in subseq_dp2_aux arr (i + 1) n new_l

-- Testing longest increasing subsequence properties:
tsubseq :: Test
tsubseq = "fib" ~: TestList[
    (subseq []) ~?= (subseq_dp []),
    (subseq [1, 2]) ~?= (subseq_dp [1, 2]),
    (subseq [2, 1]) ~?= (subseq_dp [2, 1]),
    (subseq [1, 3, 2, 4]) ~?= (subseq_dp [1, 3, 2, 4]),
    (subseq [90, 80, 91, 3, 7, 9, 10, 100, 81, 82, 93]) ~?= (subseq_dp [90, 80, 91, 3, 7, 9, 10, 100, 81, 82, 93])]

prop_subseq :: Property
prop_subseq = forAll genIntList (\i -> subseq i == subseq_dp i && subseq_dp i == subseq_dp2 i)


-- 2) Buy low, sell high
buy_sell :: [Int] -> Int
buy_sell l = buy_sell_aux l minBound

buy_sell_aux :: [Int] -> Int -> Int
buy_sell_aux (h1 : (h2 : (h3 : t))) n = let n' = buy_sell_aux' (h3 : t) h1 n in buy_sell_aux (h2 : (h3 : t)) n'
buy_sell_aux _ n = n

buy_sell_aux' :: [Int] -> Int -> Int -> Int
buy_sell_aux' [] _ n = n
buy_sell_aux' (h : t) h' n = let max_profit = max (h - h') n in buy_sell_aux' t h' max_profit

-- DP version
buy_sell_dp :: [Int] -> Int
buy_sell_dp l = let array = listArray (0, length l - 1) [i | i <- l] in 
  buy_sell_dp_aux array [minBound, minBound] maxBound 2 (length l - 1)

buy_sell_dp_aux :: Array Int Int -> [Int] -> Int -> Int -> Int -> Int
buy_sell_dp_aux share_prices profits min_share i n
  | i > n = maximum profits
  | otherwise = let new_min = min min_share (share_prices ! (i - 2)) in
                let profit = (share_prices ! i) - new_min in 
                  buy_sell_dp_aux share_prices (profit : profits) new_min (i + 1) n

-- Testing buy low/sell high properties:
prop_buy_sell :: Property
prop_buy_sell = forAll genIntList (\i -> buy_sell i == buy_sell_dp i)


-- 3) Rod cutting 
rod_cut :: [Int] -> Int
rod_cut l = let n = length l in let l' = abs_lst l in rod_cut_aux l' n

rod_cut_aux :: [Int] -> Int -> Int
rod_cut_aux _ 0 = 0
rod_cut_aux l n = let mx = minBound in traverse'' l 1 n mx

traverse'' :: [Int] -> Int -> Int -> Int -> Int
traverse'' l i n maxVal
  | i > n = maxVal
  | otherwise = let cost = (l !! (i - 1)) + rod_cut_aux l (n - i) in
                let new_max = max cost maxVal in traverse'' l (i + 1) n new_max

-- This above code runs in O(n^n) time. Hyperexponential. Oof

-- DP version
rod_cut_dp :: [Int] -> Int
rod_cut_dp l = let n = length l in let l' = abs_lst l in rod_cut_dp_aux l' n

rod_cut_dp_aux :: [Int] -> Int -> Int
rod_cut_dp_aux _ 0 = 0
rod_cut_dp_aux l n = let t = take (n + 1) (infinite_list 0) in outer_loop l t 1 n

outer_loop :: [Int] -> [Int] -> Int -> Int -> Int
outer_loop l t i n
  | i > n = t !! n
  | otherwise = outer_loop l (inner_loop l t 1 i) (i + 1) n

inner_loop :: [Int] -> [Int] -> Int -> Int -> [Int]
inner_loop l t j i
  | j > i = t
  | otherwise = let mx = max (t !! i) (l !! (j - 1) + t !! (i - j)) in 
                let t' = insert_at t 0 i mx in inner_loop l t' (j + 1) i

-- Oof that's really messy lol. But it is way more efficient than the naive version. This DP version runs in O(n^3)

-- Testing rod cutting properties:
prop_rod_cut :: Property
prop_rod_cut = forAll genIntList (\i -> rod_cut i == rod_cut_dp i)


-- 4) Edit string distancing
string_edit :: String -> String -> Int
string_edit [] s2 = length s2
string_edit s1 [] = length s1
string_edit (h1 : t1) (h2 : t2)
  | h1 == h2  = string_edit' t1 t2
  | otherwise = minimum [string_edit t1 (h2 : t2) + 1, string_edit (h1 : t1) t2 + 1, string_edit t1 t2 + 1]

string_edit' :: String -> String -> Int
string_edit' s1 s2 = opt m n 
  where m = length s1
        n = length s2
        
        opt :: Int -> Int -> Int
        opt i 0 = i 
        opt 0 j = j
        opt i j
          | s1 !! (i - 1) == s2 !! (j - 1) = opt (i - 1) (j - 1)
          | otherwise = minimum [opt (i - 1) j + 1, opt i (j - 1) + 1, opt (i - 1) (j - 1) + 1]

-- DP version
string_edit_dp :: String -> String -> Int 
string_edit_dp s1 s2 = opt m n
  where m = length s1
        n = length s2

        opt :: Int -> Int -> Int 
        opt i 0 = i
        opt 0 j = j
        opt i j
          | s1 !! (i - 1) ==  s2 !! (j - 1) = ds ! (i - 1, j - 1)
          | otherwise = minimum [ds ! (i - 1, j) + 1, ds ! (i, j - 1) + 1, ds ! (i - 1, j - 1) + 1]

        ds = listArray bounds [opt i j | (i, j) <- range bounds]
        bounds = ((0, 0), (m, n))

-- DP version 2 (using lists)
string_edit_dp2 :: String -> String -> Int 
string_edit_dp2 s1 s2 = opt m n
  where m = length s1
        n = length s2

        opt :: Int -> Int -> Int 
        opt i 0 = i
        opt 0 j = j
        opt i j
          | s1 !! (i - 1) ==  s2 !! (j - 1) = search2D list2D (i - 1) (j - 1)
          | otherwise = minimum [search2D list2D (i - 1) j + 1, search2D list2D i (j - 1) + 1, 
            search2D list2D (i - 1) (j - 1) + 1]

        indices = [(i, j) | (i, j) <- range ((0, 0), (m, n))]
        empty2D = build2D (0, 0) (m, n)
        list2D = insertBuild empty2D indices opt
        
-- Testing string editting properties:
prop_string_edit :: Property
prop_string_edit = forAll genString (\s -> forAll genString (\s' -> string_edit s s' == string_edit_dp s s'
                                    && string_edit_dp s s' == string_edit_dp2 s s'))


-- Some auxiliary functions:
-- Insert in a list at nth position
insert_at :: [Int] -> Int -> Int -> Int -> [Int]
insert_at [] _ _ _ = []
insert_at (h : t) j i e
  | j >= i = e : t
  | otherwise = h : insert_at t (j + 1) i e

-- Insert in a 2D list
insert2D :: [[Int]] -> (Int, Int) -> Int -> [[Int]]
insert2D l t e = insert2D_aux l t (0, 0) e

insert2D_aux :: [[Int]] -> (Int, Int) -> (Int, Int) -> Int -> [[Int]]
insert2D_aux [] _ _ _ = []
insert2D_aux (h : t) (u1, u2) (l1, l2) e
  | l1 > u1 = (h : t)
  | l1 == u1 = (insert_at h l2 u2 e) : insert2D_aux t (u1, u2) (l1 + 1, l2) e
  | otherwise = h : (insert2D_aux t (u1, u2) (l1 + 1, l2) e)

-- Build an empty 1D list
build_list :: Int -> Int -> [Int]
build_list i n
  | i > n = []
  | otherwise = 0 : (build_list (i + 1) n)

-- Build an empty 2D list
build2D :: (Int, Int) -> (Int, Int) -> [[Int]]
build2D (i, j) (m, n)
  | i > m = []
  | otherwise = (build_list j n) : (build2D (i + 1, j) (m, n))

insertBuild :: [[Int]] -> [(Int, Int)] -> (Int -> Int -> Int) -> [[Int]]
insertBuild l [] _ = l
insertBuild l (h : t) f = let (i, j) = h in let new2D = insert2D l h (f i j) in insertBuild new2D t f

-- Search a 2D list
search2D :: [[Int]] -> Int -> Int -> Int
search2D lst i j = let l = lst !! i in l !! j

-- Make all the integers positive in a list of integers
abs_lst :: [Int] -> [Int]
abs_lst l = foldr (\h a -> (abs h) : a) [] l

-- An infinite list of any integer
infinite_list :: Int -> [Int]
infinite_list i = i : (infinite_list i)


-- Generate arbitrary lists
genList :: forall a. (Arbitrary a) => Gen [a]
genList = sized gen
  where
    gen :: Int -> Gen [a]
    gen n =
      frequency
        [ (1, return []),
          (n, liftM2 (:) arbitrary (gen (n `div` 2)))
        ]

-- Generate Ints
genInt :: Int -> Gen Int
genInt i = choose (0, i)

-- Generate Strings
genString:: Gen String
genString = genList

-- Generate Int lists
genIntList:: Gen [Int]
genIntList = genList

-- Running all the quickChecks at once
return []
runTests :: IO Bool
runTests = $quickCheckAll


-- Running main in ghci
main :: IO ()
main = do
  _ <- runTests
  return ()
