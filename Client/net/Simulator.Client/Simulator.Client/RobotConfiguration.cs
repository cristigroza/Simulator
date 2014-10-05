using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Simulator.Client
{
    public class RobotConfiguration
    {
        
        static RobotConfiguration()
        {
            ServerIp = "127.0.0.1";
            ServerPort = 10001;
            RobotType = EnumRobotType.X80;
        }
        public static string ServerIp { get; set; }
        public static int ServerPort { get; set; }

        public static EnumRobotType RobotType { get; set; }
    }
}
