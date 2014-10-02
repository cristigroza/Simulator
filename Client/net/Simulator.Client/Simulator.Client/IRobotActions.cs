using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Simulator.Client
{
    public interface IRobotActions
    {
        void Move(int left, int right);
        int GetIr1();
    }
}
