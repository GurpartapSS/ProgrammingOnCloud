#include<iostream>
#include<WS2tcpip.h>
#pragma comment(lib, "ws2_32.lib")
using namespace std;
#include<string>

void main()
{
	string ipAddress = "127.0.0.1";
	int port = 54000;

	// Initialize Winsock
	WSADATA data;
	WORD ver = MAKEWORD(2, 2);

	int wsResult = WSAStartup(ver, &data);
	if (wsResult != 0)
	{
		cout << "cant start " << wsResult << endl;
		return;
	}

	// Create Socket
	SOCKET sock = socket(AF_INET, SOCK_STREAM, 0);
	if (sock == INVALID_SOCKET)
	{
		cerr << "sock error" << WSAGetLastError << endl;
		WSACleanup();
		return;
	}

	// Fill in hint struc
	sockaddr_in hint;
	hint.sin_family = AF_INET;
	hint.sin_port = htons(port);
	inet_pton(AF_INET, ipAddress.c_str(), &hint.sin_addr);


	//connect to server
	int connResult = connect(sock, (sockaddr*)&hint, sizeof(hint));
	if (connResult == SOCKET_ERROR) 
	{
		cerr << "cant connect to server" << WSAGetLastError << endl;
		closesocket(sock);
		WSACleanup();
		return;
	}

	//Do-while loop to send and receive data
	char buff[4096];
	string UserInput;
	do
	{
		cout << "> ";
		getline(cin, UserInput);
		if (UserInput.size() > 0)
		{
			int sendResult = send(sock, UserInput.c_str(), UserInput.size() + 1, 0);
			if (sendResult != SOCKET_ERROR)
			{
				ZeroMemory(buff, 4096);
				int bytesRec = recv(sock, buff, 4096, 0);
				if (bytesRec > 0)
				{
					cout << "<SERVER>" << string(buff, 0, bytesRec) << endl;
				}
			}
		}
	} while (UserInput.size() > 0);

	
	// close 
	closesocket(sock);
	WSACleanup();
}