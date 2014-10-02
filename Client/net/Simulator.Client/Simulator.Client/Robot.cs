using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Simulator.Client.CommandLayerImplementation;

namespace Simulator.Client
{
    public class Robot: IRobotActions
    {
        private readonly EnumRobotType _type;
        private readonly ICommandLayer _command;
        public Robot(EnumRobotType type)
        {
            _type = type;
            _command = CommandFactory.CreateCommandLayer(type);
        }


        public void Move(int left, int right)
        {
            _command.Move(left,right);
        }

        public int GetIr1()
        {
            return _command.GetIr1();
        }
    }
}
