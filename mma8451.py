from micropython import const

# Internal constants:
_MMA8451_DEFAULT_ADDRESS =        const(0x1D)

_MMA8451_REG_STATUS =             const(0x00)
_MMA8451_REG_OUT_X_MSB =          const(0x01)
_MMA8451_REG_OUT_X_LSB =          const(0x02)
_MMA8451_REG_OUT_Y_MSB =          const(0x03)
_MMA8451_REG_OUT_Y_LSB =          const(0x04)
_MMA8451_REG_OUT_Z_MSB =          const(0x05)
_MMA8451_REG_OUT_Z_LSB =          const(0x06)
_MMA8451_REG_RESERVED_1 =         const(0x07)
_MMA8451_REG_RESERVED_2 =         const(0x08)
_MMA8451_REG_F_SETUP =            const(0x09)
_MMA8451_REG_TRIG_CFG =           const(0x0A)
_MMA8451_REG_SYSMOD =             const(0x0B)
_MMA8451_REG_INT_SOURCE =         const(0x0C)
_MMA8451_REG_WHOAMI =             const(0x0D)
_MMA8451_REG_XYZ_DATA_CFG =       const(0x0E)
_MMA8451_REG_HP_FILTER_CUTOFF =   const(0x0F)
_MMA8451_REG_PL_STATUS =          const(0x10)
_MMA8451_REG_PL_CFG =             const(0x11)
_MMA8451_REG_PL_COUNT =           const(0x12)
_MMA8451_REG_BF_ZCOMP =           const(0x13)
_MMA8451_REG_P_L_THS_REG =        const(0x14)
_MMA8451_REG_FF_MT_CFG =          const(0x15)
_MMA8451_REG_FF_MT_SRC =          const(0x16)
_MMA8451_REG_FF_MT_THS =          const(0x17)
_MMA8451_REG_FF_MT_COUNT =        const(0x18)
_MMA8451_REG_RESERVED_3 =         const(0x19)
_MMA8451_REG_RESERVED_4 =         const(0x1A)
_MMA8451_REG_RESERVED_5 =         const(0x1B)
_MMA8451_REG_RESERVED_6 =         const(0x1C)
_MMA8451_REG_TRANSIENT_CFG =      const(0x1D)
_MMA8451_REG_TRANSIENT_SRC =      const(0x1E)
_MMA8451_REG_TRANSIENT_THS =      const(0x1F)
_MMA8451_REG_TRANSIENT_COUNT =    const(0x20)
_MMA8451_REG_PULSE_CFG =          const(0x21)
_MMA8451_REG_PULSE_SRC =          const(0x22)
_MMA8451_REG_PULSE_THSX =         const(0x23)
_MMA8451_REG_PULSE_THSY =         const(0x24)
_MMA8451_REG_PULSE_THSZ =         const(0x25)
_MMA8451_REG_PULSE_TMLT =         const(0x26)
_MMA8451_REG_PULSE_LTCY =         const(0x27)
_MMA8451_REG_PULSE_WIND =         const(0x28)
_MMA8451_REG_ASLP_COUNT =         const(0x29)
_MMA8451_REG_CTRL_REG1 =          const(0x2A)
_MMA8451_REG_CTRL_REG2 =          const(0x2B)
_MMA8451_REG_CTRL_REG3 =          const(0x2C)
_MMA8451_REG_CTRL_REG4 =          const(0x2D)
_MMA8451_REG_CTRL_REG5 =          const(0x2E)
_MMA8451_REG_OFF_X =              const(0x2F)
_MMA8451_REG_OFF_Y =              const(0x30)
_MMA8451_REG_OFF_Z =              const(0x31)

_MMA8451_DATARATE_MASK = const(0b111)
_SENSORS_GRAVITY_EARTH = 9.80665

# External user-facing constants:
PL_PUF = 0  # Portrait, up, front
PL_PUB = 1  # Portrait, up, back
PL_PDF = 2  # Portrait, down, front
PL_PDB = 3  # Portrait, down, back
PL_LRF = 4  # Landscape, right, front
PL_LRB = 5  # Landscape, right, back
PL_LLF = 6  # Landscape, left, front
PL_LLB = 7  # Landscape, left, back
RANGE_8G = 0b10  # +/- 8g
RANGE_4G = 0b01  # +/- 4g (default value)
RANGE_2G = 0b00  # +/- 2g
DATARATE_800HZ = 0b000  #  800Hz
DATARATE_400HZ = 0b001  #  400Hz
DATARATE_200HZ = 0b010  #  200Hz
DATARATE_100HZ = 0b011  #  100Hz
DATARATE_50HZ = 0b100  #   50Hz
DATARATE_12_5HZ = 0b101  # 12.5Hz
DATARATE_6_25HZ = 0b110  # 6.25Hz
DATARATE_1_56HZ = 0b111  # 1.56Hz

MODE_STANDBY = 0b00
MODE_ACTIVE = 0b01

class MMA8451:
    def __init__(self, i2c, addr=_MMA8451_DEFAULT_ADDRESS):
        self.i2c = i2c
        self.addr = addr
        self.val_u8 = bytearray(1)
        self.active = False

    def _read_u8(self, address):
        self.i2c.readfrom_mem_into(self.addr, address, self.val_u8)
        return self.val_u8[0]

    def _write_u8(self, address, val):
        self.i2c.writeto_mem(self.addr, address, val)
        
    def set_mode_standby(self):
        val = _read_u8(self, _MMA8451_REG_CTRL_REG1)
        val &= ~0x01
        _write_u8(self, _MMA8451_REG_CTRL_REG1, val)
        self.active = False
        
    def set_mode_active(self):
        val = _read_u8(self, _MMA8451_REG_CTRL_REG1)
        val |= 0x01
        _write_u8(self, _MMA8451_REG_CTRL_REG1, val)
        self.active = True
        
    def is_mode_active(self):
        return self.active
        
    def set_range(self, range):
        if (is_mode_active()):
            return false
                   
        val = _read_u8(self, _MMA8451_REG_XYZ_DATA_CFG)
        val &= ~0x03
        val |= (range & 0x03)
        _write_u8(self, _MMA8451_REG_XYZ_DATA_CFG, val)
        return true
           
    def set_data_rate(self, rate):
        if (is_mode_active()):
            return false
            
        val = _read_u8(self, _MMA8451_REG_CTRL_REG1)
        val &= ~0x38
        val |= ((rate & 0x07) << 3)
        _write_u8(self, _MMA8451_REG_CTRL_REG1, val)
        return true
    
    def set_oversampling_mode(self, mode):
        if (is_mode_active()):
            return false
            
        val = _read_u8(self, _MMA8451_REG_CTRL_REG2)
        val &= ~0x03
        val |= mode & 0x03
        _write_u8(self, _MMA8451_REG_CTRL_REG2, val)
        return true
            