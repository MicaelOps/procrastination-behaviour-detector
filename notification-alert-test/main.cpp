

#include <windows.h>
#include <time.h>
#include <iostream>

// prototype
LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam);

HWND hWnd, hActiveWindow, hPrevWindow;
UINT dwSize;
WCHAR keyChar;

RAWINPUTDEVICE rid[2];

// statistics
CHAR previous_window_title [256] = "";
INT keys_pressed = 0, mouse_clicks = 0, tabs_changed;
DOUBLE mouse_travel = 0.0;

LONG last_x = 0, last_y = 0;

DWORD scheduledTime = GetTickCount() + 3000;

LRESULT CALLBACK mouseHookProc(int nCode, WPARAM wParam, LPARAM lParam)
{

    if(lParam != WM_MOUSEMOVE && lParam == WM_MOUSEWHEEL) {
        mouse_clicks++;
    }

    return CallNextHookEx(NULL, nCode, wParam, lParam);
}

// Main
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow)
{
    MSG msg          = {0};
    WNDCLASS wc      = {0};

    wc.lpfnWndProc   = WndProc;
    wc.hInstance     = hInstance;
    wc.lpszClassName = "kl";


    HHOOK mouseHook = SetWindowsHookEx(WH_MOUSE_LL,mouseHookProc,hInstance,NULL);
    
    RegisterClass(&wc);
    hWnd = CreateWindow(wc.lpszClassName, NULL, 0, 0, 0, 0, 0, HWND_MESSAGE, NULL, hInstance, NULL);

    while(GetMessage(&msg, hWnd, 0, 0) ){
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    UnhookWindowsHookEx(mouseHook);
    return msg.wParam;
}

void wl(UINT keyChar){
    CHAR window_title [256] = "";

    SYSTEMTIME curr_time;

    GetLocalTime(&curr_time);

    hActiveWindow = GetForegroundWindow();
    GetWindowTextA(hActiveWindow, window_title, 256);

    if(strcmp(window_title, previous_window_title) != 0) {
        tabs_changed++;
        strcpy_s(previous_window_title, 256, window_title);
    }

    keys_pressed++;

    if( (hActiveWindow != hPrevWindow) && (keyChar != 13) ){
        hPrevWindow = hActiveWindow;
    }


}

// WndProc is called when a window message is sent to the handle of the window
LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam)
{
    switch(message){

        case WM_CREATE:{

            // register interest in raw data
            rid[0].dwFlags = RIDEV_NOLEGACY|RIDEV_INPUTSINK|RIDEV_NOHOTKEYS;	// ignore legacy messages, hotkeys and receive system wide keystrokes
            rid[0].usUsagePage = 1;											// raw keyboard data only
            rid[0].usUsage = 6;
            rid[0].hwndTarget = hWnd;

            rid[1].usUsagePage = 0x01; //Mouse
            rid[1].usUsage = 0x02;
            rid[1].dwFlags = RIDEV_INPUTSINK;
            rid[1].hwndTarget = hWnd;

            RegisterRawInputDevices(rid, 2, sizeof(rid[0]));
            break;
        }// end case WM_CREATE

        case WM_DESTROY:{
            PostQuitMessage(0);
            break;
        }// end case WM_DESTROY

        case WM_INPUT:{


            if( GetRawInputData((HRAWINPUT)lParam, RID_INPUT, NULL, &dwSize, sizeof(RAWINPUTHEADER)) == -1){
                PostQuitMessage(0);
                break;
            }

            auto lpb = new BYTE[dwSize];
            if(lpb == NULL){
                PostQuitMessage(0);
                break;
            }

            if( GetRawInputData((HRAWINPUT)lParam, RID_INPUT, lpb, &dwSize, sizeof(RAWINPUTHEADER)) != dwSize){
                delete[] lpb;
                PostQuitMessage(0);
                break;
            }

            auto raw = (PRAWINPUT)lpb;
            UINT Event;

            if(raw->header.dwType == RIM_TYPEMOUSE) {
                std::cout << "received mouse input";

                DWORD currentTime = GetTickCount();
                if(currentTime > scheduledTime) {

                    scheduledTime = currentTime + 3000;

                    if(last_x == 0 || last_y == 0){
                        last_x = raw->data.mouse.lLastX;
                        last_y = raw->data.mouse.lLastY;
                    } else {
                        LONG x_diff = abs(raw->data.mouse.lLastX - last_x);
                        LONG y_diff = abs(raw->data.mouse.lLastY - last_y);
                        double distance = sqrt((x_diff * x_diff) + (y_diff * y_diff));
                        mouse_travel += distance;
                    }
                }

                delete[] lpb;	// free this now
            } else {
                Event = raw->data.keyboard.Message;
                keyChar = MapVirtualKey(raw->data.keyboard.VKey, MAPVK_VK_TO_CHAR);
                delete[] lpb;	// free this now

                if(Event == WM_KEYDOWN)
                    wl(keyChar);
            }
        }
        default:
            return DefWindowProc(hWnd, message, wParam, lParam);
    }
    return 0;
}
