from abc import ABC, abstractmethod
import logging


# ===============================
# LOGGING CONFIG
# ===============================

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)



# ===============================
# ABSTRACT BASE CLASS
# ===============================

class BaseDevice(ABC):

    factory_name = "Rikkei Smart Factory"
    base_maintenance_cost = 1000000


    def __init__(self, device_code, device_name):

        if not self.validate_device_code(device_code):

            raise ValueError(
                "ERR-IOT-01"
            )


        self.device_code = device_code
        self.device_name = device_name



        # private attribute
        self.__operating_hours = 0



    # ==========================
    # PROPERTY
    # read only
    # ==========================

    @property
    def operating_hours(self):

        return self.__operating_hours



    def add_operating_hours(self,hours):

        if hours <=0:

            raise ValueError(
            "ERR-IOT-03"
            )


        self.__operating_hours += hours




    # ==========================
    # ABSTRACT METHODS
    # ==========================


    @abstractmethod
    def track_performance(self):

        pass



    @abstractmethod
    def run_diagnostic(self):

        pass





    # ==========================
    # OPERATOR OVERLOADING
    # ==========================


    def __add__(self,other):

        if not isinstance(other,BaseDevice):

            raise TypeError(
            "ERR-IOT-04"
            )


        return (
            self.operating_hours
            +
            other.operating_hours
        )




    def __lt__(self,other):

        if not isinstance(other,BaseDevice):

            raise TypeError(
            "ERR-IOT-04"
            )


        return (
            self.operating_hours
            <
            other.operating_hours
        )





    # ==========================
    # STATIC METHOD
    # ==========================


    @staticmethod
    def validate_device_code(device_code):

        return (
            isinstance(device_code,str)
            and len(device_code)==10
            and device_code[0].isalpha()
        )





    # ==========================
    # CLASS METHOD
    # ==========================


    @classmethod
    def update_maintenance_cost(cls,new_cost):

        if new_cost <=0:

            raise ValueError(
            "Invalid maintenance cost"
            )


        cls.base_maintenance_cost = new_cost





# ===============================
# PRODUCTION ROBOT
# ===============================


class ProductionRobot(BaseDevice):


    def __init__(self,device_code,device_name):

        super().__init__(
            device_code,
            device_name.strip().upper()
        )


        self.completed_products = 0




    def track_performance(self):

        if self.completed_products <=0:

            return 0


        oee = (
            self.completed_products
            /
            20000
            *
            100
        )


        return min(oee,100)



    def run_diagnostic(self):


        if self.completed_products >10000:

            return (
            "Cảnh báo: Cần bảo dưỡng robot"
            )


        return "Robot hoạt động bình thường"





# ===============================
# THERMAL SENSOR
# ===============================


class ThermalSensor(BaseDevice):


    def __init__(self,device_code,device_name):

        super().__init__(
            device_code,
            device_name.strip().upper()
        )


        self.current_temperature = 0
        self.safety_threshold = 80




    def track_performance(self):

        return (
            self.safety_threshold
            -
            self.current_temperature
        )





    def run_diagnostic(self):


        if self.current_temperature > self.safety_threshold:

            return (
            f"Nguy hiểm: Vượt ngưỡng nhiệt!"
            f" {self.current_temperature}°C"
            )


        return "Nhiệt độ an toàn"






# ===============================
# HYBRID DEVICE
# MULTIPLE INHERITANCE
# ===============================


class HybridSmartActuator(
    ProductionRobot,
    ThermalSensor
):


    def track_performance(self):

        robot_score = (
            self.completed_products / 20000 *100
        )


        temp_score = (
            self.safety_threshold
            -
            self.current_temperature
        )


        return (
            robot_score
            +
            temp_score
        ) /2




    def run_diagnostic(self):

        robot_check = ProductionRobot.run_diagnostic(self)

        temp_check = ThermalSensor.run_diagnostic(self)


        return (
            robot_check
            +
            " | "
            +
            temp_check
        )







# ===============================
# DUCK TYPING GATEWAY
# ===============================


class MQTTEngineGateway:


    def process_stream(self,device):

        print(
        f"""
[MQTT Engine]
Đang gửi dữ liệu IoT...

Device:
{device.device_code}

Export thành công
"""
        )





class ERPReportGateway:


    def process_stream(self,device):

        print(
        f"""
[ERP Gateway]
Đồng bộ báo cáo thiết bị:
{device.device_code}
"""
        )






def export_telemetry_data(
        data_gateway,
        device_object
):


    try:

        data_gateway.process_stream(
            device_object
        )


    except AttributeError:


        logging.error(
        "ERR-IOT-05"
        )






# ===============================
# CLI
# ===============================


devices_list=[]

current_device=None





def create_device():


    global current_device


    print(
"""
1. Production Robot
2. Thermal Sensor
3. Hybrid Smart Actuator
"""
)


    choice=input()


    code=input("Device code: ")

    name=input("Device name: ")



    try:


        if choice=="1":

            device=ProductionRobot(
                code,
                name
            )


        elif choice=="2":

            device=ThermalSensor(
                code,
                name
            )


        elif choice=="3":

            device=HybridSmartActuator(
                code,
                name
            )


        else:

            raise ValueError("Invalid")



        devices_list.append(device)

        current_device=device


        print(
        "Đăng ký thành công"
        )


    except ValueError:

        logging.error(
        "ERR-IOT-01"
        )





def show_info():


    if current_device is None:

        logging.error(
        "ERR-IOT-02"
        )

        return



    print(
f"""
Device:
{current_device.__class__.__name__}

Factory:
{current_device.factory_name}

Code:
{current_device.device_code}

Name:
{current_device.device_name}

Hours:
{current_device.operating_hours}


MRO:

{current_device.__class__.mro()}

"""
)





def update_data():


    try:


        hours=int(
        input("Operating hours: ")
        )


        current_device.add_operating_hours(
            hours
        )



        if isinstance(
            current_device,
            ProductionRobot
        ):


            products=int(
            input("Products: ")
            )

            current_device.completed_products += products




        print(
        "OEE:",
        current_device.track_performance()
        )



    except:


        logging.error(
        "ERR-IOT-03"
        )





def menu():


    global current_device


    while True:


        print(
"""
===== RIKKEI SMART FACTORY IOT =====

1.Register
2.Info + MRO
3.Update Performance
4.Diagnostic
5.Operator
6.Export
7.Exit

"""
)


        try:

            choice=int(input())


        except:

            logging.error(
            "ERR-IOT-06"
            )

            continue



        if choice==1:

            create_device()



        elif choice==2:

            show_info()

        elif choice==3:

            update_data()

        elif choice==4:

            print(
            current_device.run_diagnostic()
            )

        elif choice==5:

            if len(devices_list)<2:
                print("Need 2 devices")
                continue

            a=devices_list[0]
            b=devices_list[1]

            print(
            "Total hours:",
            a+b
            )


            print(
            "A < B:",
            a<b
            )

        elif choice==6:
            gateway=MQTTEngineGateway()
            export_telemetry_data(
                gateway,
                current_device
            )
        elif choice==7:
            break
        else:
            logging.error(
            "ERR-IOT-06"
            )

menu()