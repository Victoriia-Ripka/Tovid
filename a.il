// Referenced Assemblies.
.assembly extern mscorlib
{
  .publickeytoken = (B7 7A 5C 56 19 34 E0 89 ) 
  .ver 4:0:0:0
}

// Our assembly.
.assembly a
{
  .hash algorithm 0x00008004
  .ver 0:0:0:0
}

.module a.exe

// Definition of Program class.
.class private auto ansi beforefieldinit Program
  extends [mscorlib]System.Object
{

    .method private hidebysig static void Main(string[] args) cil managed
    {
    .locals (
       [0]  int32 a,
       [1]  bool b,
       [2]  float32 f,
       [3]  int32 k,
       [4]  string str,
       [5]  int32 m
     )
       [6]  float32 h
     )
       [7]  int32 five
     )
       [8]  string done
     )

   .entrypoint
   //.maxstack  8
	ldloca h
	ldc.r4 10.1
	ldc.r4 5.2
	add
	stind.r4
	ldloca a
	ldc.i4 2
	stind.i4
	ldloca a
	ldloc a
	ldc.i4 3
	add
	stind.i4
	ldloca b
	ldc.i4 1
	ldloca b
	ldloc b
	ldloca k
	ldc.i4 10
	stind.i4
	ldloca str
	ldloca five
	ldc.i4 5
	stind.i4
	ldloca done
	ldloc str
	call string [mscorlib]System.Console::ReadLine()
	stind.i4
	ldloca f
	ldloc a
	conv.r4
	ldc.i4 2
	ldc.i4 3
	ldc.i4 3
	ldc.i4 2
	div
	add
	stind.i4
	ldloca b
	ldloc a
	ldloc a
	add
	ldloc five
	clt
	stloc.s b
	ldloc a
	call void [mscorlib]System.Console::WriteLine(int32)
	ldloc f
	call void [mscorlib]System.Console::WriteLine(float32)
	ldloc b
	call void [mscorlib]System.Console::WriteLine(bool)
	ldloc "\n"
	call void [mscorlib]System.Console::WriteLine(bool)
	ldloc done
	call void [mscorlib]System.Console::WriteLine(string)
	ldloc a
	ldc.i4 15
	ceq
	brfalse m1
	br m2
m1:
	ldloc a
	ldloc a
	add
	ldloc a
	ldc.i4 3
	mul
	clt
	brtrue m3
	ldloc a
	ldc.i4 2
	cgt
	brfalse m4
	br m5
m4:
m5:
m3:
m2:
	br m6
m6:
	ldloca m
	ldc.i4 5
	stind.i4
	ldloc m
	ldc.i4 0
	clt
	brtrue m8
	br m7
m7:
	br m8
	ldloc m
	ldc.i4 0
	cgt
	brfalse m9
	ldloc "Not yet!"
	call void [mscorlib]System.Console::WriteLine(int32)
	br m10
m9:
	ldloc done
	call void [mscorlib]System.Console::WriteLine(string)
m10:
	br m6
m8:
	ldstr "a = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  a
	call void [mscorlib]System.Console::WriteLine(int32) 
	ldstr "b = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  b
	call void [mscorlib]System.Console::WriteLine(bool) 
	ldstr "f = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  f
	call void [mscorlib]System.Console::WriteLine(float32) 
	ldstr "k = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  k
	call void [mscorlib]System.Console::WriteLine(int32) 
	ldstr "str = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  str
	call void [mscorlib]System.Console::WriteLine(string) 
	ldstr "m = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  m
	call void [mscorlib]System.Console::WriteLine(int32) 
	ldstr "h = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  h
	call void [mscorlib]System.Console::WriteLine(float32) 
	ldstr "five = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  five
	call void [mscorlib]System.Console::WriteLine(int32) 
	ldstr "done = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  done
	call void [mscorlib]System.Console::WriteLine(string) 
	ret    
}
}