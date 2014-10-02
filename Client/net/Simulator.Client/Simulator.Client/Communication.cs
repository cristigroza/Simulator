using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

namespace Simulator.Client
{
    public class Communication
    {
        private readonly StreamWriter _streamWriter;
        private readonly StreamReader _streamReader;
        public Communication()
        {
            //TODO Use MEF to descover server configurations
            var tcpClient = new TcpClient(Configuration.ServerIp, Configuration.ServerPort);
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

            var ret = _streamReader.ReadLine() ?? string.Empty;
            ret = (ret.Length > 1 ? ret.Substring(0, ret.Length - 1) : ret).ToLower();
            return ret;
        }

    }
}
