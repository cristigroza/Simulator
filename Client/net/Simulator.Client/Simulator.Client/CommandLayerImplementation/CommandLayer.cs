namespace Simulator.Client.CommandLayerImplementation
{
    internal class CommandLayer : ICommandLayer
    {
        private readonly Communication _communication;
        public CommandLayer()
        {
            _communication = new Communication();

        }
        public void Move(int left, int right)
        {
            _communication.SendCommand("");
        }

        public int GetIr1()
        {
            return int.Parse(_communication.GetCommand());
        }
    }
}
