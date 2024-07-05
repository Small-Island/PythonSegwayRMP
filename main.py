import numpy as np
import serial

MPS_TO_COUNTS = 322
DPS_TO_COUNTS_ = 7.8

def IntListToBytes(arg_list):
    b = b''
    for e in arg_list:
        b = b + e.to_bytes(1, 'big')
    return b
def BytesToStringIn0Xxx(arg_bytes):
    return ''.join([r'\x{:02x}'.format(e) for e in arg_bytes])

def computeChecksum(arg_packet):
  checksum = 0
  checksum_hi = 0
  
  for i in range(0, 17):
    checksum += arg_packet[i]
  
  checksum_hi = checksum >> 8
  checksum &= 0xff
  checksum += checksum_hi
  checksum_hi = checksum >> 8
  checksum &= 0xff
  checksum += checksum_hi
  checksum = (~checksum + 1) & 0xff
  return checksum

# this->StartReadingContinuously_();
# void SegwayRMP::StartReadingContinuously_() {
#   this->continuously_reading_ = true;
#   this->read_thread_ =
#     boost::thread(&SegwayRMP::ReadContinuously_, this);
#   this->callback_execution_thread_ =
#     boost::thread(&SegwayRMP::ExecuteCallbacks_, this);
# }
# void SegwayRMP::ReadContinuously_() {
#     Packet packet;
#     while (this->continuously_reading_) {
#         try {
#             this->rmp_io_->getPacket(packet);
#             this->ProcessPacket_(packet);
#             this->no_data_from_segway = false;
#         } catch (PacketRetrievalException &e) {
#             if (e.error_number() == 2) { // Failed Checksum
#                 this->error_("Checksum mismatch...");
#             }
#             else if (e.error_number() == 3) { // No packet received
#                 // this->error_("No data from Segway...");
#                 this->no_data_from_segway = true;
#             }
#             else {
#                 this->handle_exception_(e);
#             }
#         }
#     }
# }

# ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)

packet = b'\xF0\x55\x00\x00\x00\x00'
linear_velocity = 4 # m/s
angular_velocity = 0 # deg/s
packet += b'\x04'           # id upper
packet += b'\x13'           # id lower
packet += b'\x00'           # CAN Bus Channel
packet += int(linear_velocity * MPS_TO_COUNTS).to_bytes(2, 'big', signed=True)
packet += int(angular_velocity * MPS_TO_COUNTS).to_bytes(2, 'big', signed=True)
packet += b'\x00\x00\x00\x00'
packet += computeChecksum(packet).to_bytes(1, 'big', signed=False)
print('len', len(packet),  BytesToStringIn0Xxx(packet))

msg = IntListToBytes(packet)

# ser.write(msg)
# ser.close()