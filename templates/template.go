package main

// {problem}
// {url}
// {author}
// {lang}

import "os"
import "fmt"

func main() {
   out := bufio.NewWriter(os.Stdout)
   fmt.Fprintf(out, "Hello {name}!")
   out.Flush()
}
