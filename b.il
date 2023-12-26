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
       [1]  int32 i,
       [2]  int32 l,
	ldstr ""
	call void [mscorlib]System.Console::WriteLine(string)
	ldloca a
	ldc.i4 3
	stind.i4
	ldloc a
	call void [mscorlib]System.Console::WriteLine(int32)
	br m1
m1:
	ldloca i
	ldc.i4 0
	stind.i4
	ldloc i
	ldc.i4 11
	clt
	brfalse m3
	br m2
m2:
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
	br m3
	ldloc i
	call void [mscorlib]System.Console::WriteLine(int32)
	ldloca a
	call string [mscorlib]System.Console::ReadLine()
	stind.ref
	br m4
m4:
	ldloca l
	ldc.i4 10
	stind.i4
	ldloc l
	ldc.i4 12
	clt
	brfalse m6
	br m5
m5:
	ldloca l
	ldloc l
	ldc.i4 1
	add
	stind.i4
	ldloca l
	ldloc l
	ldc.i4 1
	add
	stind.i4
	ldloca l
	ldloc l
	ldc.i4 1
	add
	stind.i4
	ldloca l
	ldloc l
	ldc.i4 1
	add
	stind.i4
	ldloca l
	ldloc l
	ldc.i4 1
	add
	stind.i4
	ldloca l
	ldloc l
	ldc.i4 1
	add
	stind.i4
	ldloca l
	ldloc l
	ldc.i4 1
	add
	stind.i4
	ldloca l
	ldloc l
	ldc.i4 1
	add
	stind.i4
	ldloca l
	ldloc l
	ldc.i4 1
	add
	stind.i4
	ldloca l
	ldloc l
	ldc.i4 1
	add
	stind.i4
	ldloca l
	ldloc l
	ldc.i4 1
	add
	stind.i4
	ldloca l
	ldloc l
	ldc.i4 1
	add
	stind.i4
	br m6
	ldloc l
	call void [mscorlib]System.Console::WriteLine(int32)
	br m4
m6:
	br m1
m3:

ldstr ""call void [mscorlib]System.Console::WriteLine(string)
ldstr ""
call void [mscorlib]System.Console::WriteLine(string)	ret    
}
}