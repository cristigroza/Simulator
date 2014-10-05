using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

namespace Simulator.Client
{
    class Communication
    {
        private readonly StreamWriter _streamWriter;
        private readonly StreamReader _streamReader;
        public Communication()
        {
            var tcpClient = new TcpClient(RobotConfiguration.ServerIp, RobotConfiguration.ServerPort);
            var networkStream = tcpClient.GetStream();
            _streamWriter = new StreamWriter(networkStream) { AutoFlush = true };
            _streamReader = new StreamReader(networkStream);
        }

        public void SendCommand(string command)
        {
            _streamWriter.WriteLine(command);
        }

        public string GetCommand()
        {
    
            var buffer =  new char[1024];
            var ret = _streamReader.Read(buffer,0,1024);
          
            return ret.ToString();
        }

    }
}
