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

    .entrypoint
    .maxstack  8
	.locals (
       [0]  int32 a,
       [1]  bool b,
       [2]  string s,
       [3]  float32 f,
       [4]  int32 k,
       [5]  string str,
       [6]  int32 yes,
       [7]  int32 no,
       [8]  int32 m,
       [9]  int32 i,
       [10]  float32 h,
       [11]  int32 five,
       [12]  string done
    )
	ldloca h
	ldc.r4 10.1
	ldc.r4 5.2
	add
	stind.r4
	ldloca a
	ldc.i4 2
	neg
	stind.i4
	ldloca a
	ldloc a
	ldc.i4 3
	add
	stind.i4
	ldloca b
	ldc.i4 1
	stind.i4
	ldloca b
	ldloc b
	neg
	stind.i4
	ldloca s
	ldstr "f"
	stind.ref
	ldloca k
	ldc.i4 10
	stind.i4
	ldloca str
	ldstr "yesyes"
	stind.ref
	ldloca five
	ldc.i4 5
	stind.i4
	ldloca done
	ldstr "Done!"
	stind.ref
	ldloca f
	conv.i4
	ldloc a
	conv.r4
	ldc.i4 2
	ldc.i4 3
	call float64 [mscorlib]System.Math::Pow(float64, float64)
	call float64 [mscorlib]System.Math::Pow(float64, float64)
	ldc.i4 3
	conv.r4
	ldc.i4 2
	conv.r4
	div
	add
	stind.r4
	ldloca b
	ldloc a
	ldloc a
	add
	ldloc five
	clt
	stind.i4
	ldloc a
	call void [mscorlib]System.Console::WriteLine(int32)
	ldloc b
	call void [mscorlib]System.Console::WriteLine(bool)
	ldloc f
	call void [mscorlib]System.Console::WriteLine(float32)
	ldstr "\n"
	call void [mscorlib]System.Console::WriteLine(string)
	ldloc done
	call void [mscorlib]System.Console::WriteLine(string)
	ldloc a
	ldc.i4 15
	ceq
	brfalse m1
	ldloca yes
	ldc.i4 10
	stind.i4
	ldloc yes
	call void [mscorlib]System.Console::WriteLine(int32)
	br m2
m1:
	ldloca no
	ldc.i4 7
	stind.i4
	ldloc no
	call void [mscorlib]System.Console::WriteLine(int32)
	ldloc a
	ldloc a
	add
	ldloc a
	ldc.i4 3
	mul
	clt
	ldc.i4 0
	ceq
	brfalse m3
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
	ldc.i4 10
	stind.i4
	ldloc m
	ldc.i4 1
	clt
	ldc.i4 0
	ceq
	brfalse m8
	br m7
m7:
	ldloca m
	ldloc m
	ldc.i4 1
	sub
	stind.i4
	ldloca m
	ldloc m
	ldc.i4 1
	sub
	stind.i4
	ldloca m
	ldloc m
	ldc.i4 1
	sub
	stind.i4
	ldloca m
	ldloc m
	ldc.i4 1
	sub
	stind.i4
	ldloca m
	ldloc m
	ldc.i4 1
	sub
	stind.i4
	ldloca m
	ldloc m
	ldc.i4 1
	sub
	stind.i4
	ldloca m
	ldloc m
	ldc.i4 1
	sub
	stind.i4
	ldloca m
	ldloc m
	ldc.i4 1
	sub
	stind.i4
	ldloca m
	ldloc m
	ldc.i4 1
	sub
	stind.i4
	br m8
	ldloc m
	ldc.i4 1
	cgt
	brfalse m9
	ldstr "Not yet!"
	call void [mscorlib]System.Console::WriteLine(string)
	br m10
m9:
	ldloc done
	call void [mscorlib]System.Console::WriteLine(string)
m10:
	ldloc m
	call void [mscorlib]System.Console::WriteLine(int32)
	br m6
m8:
	br m11
m11:
	ldloca i
	ldc.i4 0
	stind.i4
	ldloc i
	ldc.i4 11
	clt
	brfalse m13
	br m12
m12:
	ldloca i
	ldloc i
	ldc.i4 1
	add
	stind.i4
	ldloca i
	ldloc i
	ldc.i4 1
	add
	stind.i4
	ldloca i
	ldloc i
	ldc.i4 1
	add
	stind.i4
	ldloca i
	ldloc i
	ldc.i4 1
	add
	stind.i4
	ldloca i
	ldloc i
	ldc.i4 1
	add
	stind.i4
	ldloca i
	ldloc i
	ldc.i4 1
	add
	stind.i4
	ldloca i
	ldloc i
	ldc.i4 1
	add
	stind.i4
	ldloca i
	ldloc i
	ldc.i4 1
	add
	stind.i4
	ldloca i
	ldloc i
	ldc.i4 1
	add
	stind.i4
	ldloca i
	ldloc i
	ldc.i4 1
	add
	stind.i4
	ldloca i
	ldloc i
	ldc.i4 1
	add
	stind.i4
	br m13
	ldloc i
	call void [mscorlib]System.Console::WriteLine(int32)
	br m11
m13:
	ldstr "a = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  a
	call void [mscorlib]System.Console::WriteLine(int32) 
	ldstr "b = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  b
	call void [mscorlib]System.Console::WriteLine(bool) 
	ldstr "s = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  s
	call void [mscorlib]System.Console::WriteLine(string) 
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
	ldstr "yes = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  yes
	call void [mscorlib]System.Console::WriteLine(int32) 
	ldstr "no = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  no
	call void [mscorlib]System.Console::WriteLine(int32) 
	ldstr "m = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  m
	call void [mscorlib]System.Console::WriteLine(int32) 
	ldstr "i = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  i
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
	ldstr "Press any key to continue..."
	call void [mscorlib]System.Console::WriteLine(string)
	ret    
}
}