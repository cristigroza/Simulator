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
        private object _syncObj = new object();
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
            lock (_syncObj)
            {
                _streamWriter.WriteLine(command);
            }
        }

        public string GetCommand()
        {

            lock (_syncObj)
            {
                var ret = _streamReader.ReadLine();

                return ret;
            }
            
        }

    }
}
