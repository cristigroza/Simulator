namespace Simulator.Client.CommandLayerImplementation
{
    public class CommandFactory
    {
        internal static ICommandLayer CreateCommandLayer(EnumRobotType type)
        {
            switch (type)
            {
                case EnumRobotType.X80: return new CommandLayer();
                case EnumRobotType.X80H: return new CommandLayer(); 
                case EnumRobotType.I90: return new CommandLayer(); 
                case EnumRobotType.Drk8080: return new CommandLayer(); 
            }

            return new CommandLayer();
        }
    }
}
