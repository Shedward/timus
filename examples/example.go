package main

import "os"
import "fmt"
import "bufio"
import "strings"
import "strconv"

func main() {
   in := bufio.NewReader(os.Stdin)
   out := bufio.NewWriter(os.Stdout)
   text, _ := in.ReadString(0)
   a := strings.Fields(text)
   var sum int64
   for i := len(a) - 1; i >= 0; i-- {
      x, _ := strconv.ParseInt(a[i],10, 64)
      sum += x
   }
   fmt.Fprintf(out, "%d\n", sum)
   out.Flush()
}