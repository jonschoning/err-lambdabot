import Codec.Binary.UTF8.String
import Text.Printf
import System.IO
import System.IO.Error

main :: IO ()
main = tryIOError (hGetLine stdin) >>= either (const $ return ()) go
  where 
    go x = do
      let ld = decodeString x
      printf ld
      printf "\n"
      main
    
