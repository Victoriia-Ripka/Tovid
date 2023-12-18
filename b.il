// Referenced Assemblies.
.assembly extern mscorlib
{
  .publickeytoken = (B7 7A 5C 56 19 34 E0 89 ) 
  .ver 4:0:0:0
}

// Our assembly.
.assembly b
{
  .hash algorithm 0x00008004
  .ver 0:0:0:0
}

.module b.exe

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
       [1]  float32 b,
       [2]  float32 new,
       [3]  string s,
       [4]  int32 c,
       [5]  string done
    )
	ldloca a
	ldc.i4 2
	stind.i4
	ldloca b
	ldc.r4 3.1
	stind.r4
	ldloca c
	ldc.i4 4
	stind.i4
	ldloca new
	ldc.i4 0
	conv.r4
	ldc.i4 1
	conv.r4
	ldc.i4 4
	conv.r4
	conv.i4
	ldloc c
	conv.r4
	call float64 [mscorlib]System.Math::Pow(float64, float64)
	call float64 [mscorlib]System.Math::Pow(float64, float64)
	sub
	ldc.i4 3
	conv.r4
	ldc.i4 2
	conv.r4
	div
	add
	stind.r4
	ldloca s
	ldstr "hello"
	stind.ref
	ldloc a
	call void [mscorlib]System.Console::WriteLine(int32)
	ldloc b
	call void [mscorlib]System.Console::WriteLine(float32)
	ldloc c
	call void [mscorlib]System.Console::WriteLine(int32)
	ldloc s
	call void [mscorlib]System.Console::WriteLine(string)
	ldloc new
	call void [mscorlib]System.Console::WriteLine(float32)
	ldloca done
	ldstr "Done!"
	stind.ref
	ldstr "\n"
	call void [mscorlib]System.Console::WriteLine(string)
	ldloc done
	call void [mscorlib]System.Console::WriteLine(string)
	ldstr "a = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  a
	call void [mscorlib]System.Console::WriteLine(int32) 
	ldstr "b = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  b
	call void [mscorlib]System.Console::WriteLine(float32) 
	ldstr "new = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  new
	call void [mscorlib]System.Console::WriteLine(float32) 
	ldstr "s = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  s
	call void [mscorlib]System.Console::WriteLine(string) 
	ldstr "c = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  c
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