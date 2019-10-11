#include<iostream>
#include<WS2tcpip.h> // winsock library windos socket for TCP IP

#pragma comment(lib, "ws2_32.lib")
using namespace std;

void main()
{
	//initialise winsock -- connection making
	WSADATA wsData; // struc 
	WORD ver = MAKEWORD(2, 2);

	int wsOk = WSAStartup(ver, &wsData);
	if (wsOk != 0)
	{
		cerr << "Errr" << endl;
		return;
	}
	// create a socket
	SOCKET listening = socket(AF_INET, SOCK_STREAM, 0);
	if (listening == INVALID_SOCKET)
	{
		cerr << "err" << endl;
		return;
	}

	// bind ip address and port to socket
	sockaddr_in hint;
	hint.sin_family = AF_INET;
	hint.sin_port = htons(54000); //host to network short to tackle big endian and little endian prob
	hint.sin_addr.S_un.S_addr = INADDR_ANY; //bind to any address ... could also use inet_pton

	bind(listening, (sockaddr*)&hint, sizeof(hint));
								 
	// tell winsock, socket is for listerning
	listen(listening, SOMAXCONN);

	//wait for connection
	sockaddr_in client;
	int ClientSize = sizeof(client);

	SOCKET clientSocket = accept(listening, (sockaddr*)&client, &ClientSize);

	char host[NI_MAXHOST]; //name of client 
	char service[NI_MAXSERV]; // port the client is connected on
	ZeroMemory(host, NI_MAXHOST);  // same as memset(host, 0 , NI_MAXHOST)
	ZeroMemory(service, NI_MAXSERV);

	if (getnameinfo((sockaddr*)&client, sizeof(client),host,NI_MAXHOST,service,NI_MAXSERV,0)==0)
	{
		cout << host << "connected on port " << service << endl;
	}
	else
	{
		inet_ntop(AF_INET, &client.sin_addr, host, NI_MAXHOST);
		cout << host << "host connected on port"  << ntohs(client.sin_port) << endl;
	}
	//close listening socket
	closesocket(listening);
	// while loop: accept and echo message
	char buff[4096];
	while (true)
	{
		ZeroMemory(buff, 4096);
		//wait for data

		int bytesRecieved = recv(clientSocket, buff, 4096, 0);
		if (bytesRecieved == SOCKET_ERROR)
		{
			cout << "err" << endl;
			break;
		}

		if (bytesRecieved == 0)
		{
			cout << "client not connected " << endl;
			break;
		}
		// echo msg back to client
		cout << "got " << string(buff, 0, bytesRecieved) << endl;
		send(clientSocket, buff, bytesRecieved + 1, 0);
	}
	//close socket
	closesocket(clientSocket);
	//clean winsock
	WSACleanup();
}