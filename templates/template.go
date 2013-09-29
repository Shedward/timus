package main

import "os"
import "fmt"

func main() {
   out := bufio.NewWriter(os.Stdout)
   fmt.Fprintf(out, "Hello!")
   out.Flush()
}
