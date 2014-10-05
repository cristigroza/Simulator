using System;

namespace Simulator.Client.CommandLayer
{
     class CommandFactory
    {
        internal static ICommandLayer CreateCommandLayer()
        {
            switch (RobotConfiguration.RobotType)
            {
                case EnumRobotType.X80: return  new CommandRobotX80();
                case EnumRobotType.X80H: return new CommandRobotX80H();
                case EnumRobotType.I90: return new CommandRobotI90();
                case EnumRobotType.Drk8080: return new CommandRobotDRK8080(); 
            }

            throw new Exception("An invalid robot type is specified in the RobotConfiguration class.");
        }
    }
}
