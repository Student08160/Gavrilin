using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.ConstrainedExecution;
using System.Text;
using System.Threading.Tasks;
using MyApp.Models;

namespace MyApp.Models
{
    internal class Program
    {
        static void Main(string[] args)
        {
            Car car = new Car();
            car.SetMakeAndModel("Тойота", "Королла");
            car.Year = 2020;

            ElectricCar eCar = new ElectricCar();
            eCar.SetMakeAndModel("Тесла", "Model S");
            eCar.Year = 2023;
            eCar.SetBatteryCapacity(100.5);

            Console.WriteLine("Информация о Car:");
            car.PublicDisplay();

            Console.WriteLine("\nИнформация об ElectricCar:");
            eCar.PublicDisplay();
        }
    }
}
