## Clock
set_property -dict { PACKAGE_PIN AL34   IOSTANDARD LVDS } [get_ports { usrclk_n }];
set_property -dict { PACKAGE_PIN AK34   IOSTANDARD LVDS } [get_ports { usrclk_p }];

## UART
set_property -dict {PACKAGE_PIN AU33 IOSTANDARD LVCMOS18} [get_ports rx_d_in]
set_property -dict {PACKAGE_PIN AU36 IOSTANDARD LVCMOS18} [get_ports tx_d_out]

## Pusht buttons 
set_property -dict { PACKAGE_PIN AV39   IOSTANDARD LVCMOS18 } [get_ports { rst }];
set_property -dict { PACKAGE_PIN AR40   IOSTANDARD LVCMOS18 } [get_ports { pushbtn_n }];
set_property -dict { PACKAGE_PIN AU38   IOSTANDARD LVCMOS18 } [get_ports { pushbtn_e }];
set_property -dict { PACKAGE_PIN AW40   IOSTANDARD LVCMOS18 } [get_ports { pushbtn_w }];
set_property -dict { PACKAGE_PIN AP40   IOSTANDARD LVCMOS18 } [get_ports { pushbtn_s }];

## LEDs
set_property -dict { PACKAGE_PIN AM39   IOSTANDARD LVCMOS18 } [get_ports { led[0] }];
set_property -dict { PACKAGE_PIN AN39   IOSTANDARD LVCMOS18 } [get_ports { led[1] }];
set_property -dict { PACKAGE_PIN AR37   IOSTANDARD LVCMOS18 } [get_ports { led[2] }];
set_property -dict { PACKAGE_PIN AT37   IOSTANDARD LVCMOS18 } [get_ports { led[3] }];
set_property -dict { PACKAGE_PIN AR35   IOSTANDARD LVCMOS18 } [get_ports { led[4] }];
set_property -dict { PACKAGE_PIN AP41   IOSTANDARD LVCMOS18 } [get_ports { led[5] }];
set_property -dict { PACKAGE_PIN AP42   IOSTANDARD LVCMOS18 } [get_ports { led[6] }];
set_property -dict { PACKAGE_PIN AU39   IOSTANDARD LVCMOS18 } [get_ports { led[7] }];


## GPIO (FMC1)
set_property -dict { PACKAGE_PIN J25   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j2_1 }];
set_property -dict { PACKAGE_PIN M22   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j2_2 }];
set_property -dict { PACKAGE_PIN J26   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j2_3 }];
set_property -dict { PACKAGE_PIN L22   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j2_4 }];
set_property -dict { PACKAGE_PIN H28   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j2_5_to_36[0] }];
set_property -dict { PACKAGE_PIN K22   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j2_5_to_36[1] }];
set_property -dict { PACKAGE_PIN H29   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j2_5_to_36[2] }];
set_property -dict { PACKAGE_PIN J22   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j2_5_to_36[3] }];
set_property -dict { PACKAGE_PIN K28   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j2_5_to_36[4] }];
set_property -dict { PACKAGE_PIN K24   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j2_5_to_36[5] }];
set_property -dict { PACKAGE_PIN J28   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j2_5_to_36[6] }];
set_property -dict { PACKAGE_PIN K25   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j2_5_to_36[7] }];
set_property -dict { PACKAGE_PIN G28   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j2_5_to_36[8] }];
set_property -dict { PACKAGE_PIN P25   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j2_5_to_36[9] }];
set_property -dict { PACKAGE_PIN G29   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j2_5_to_36[10] }];
set_property -dict { PACKAGE_PIN P26   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j2_5_to_36[11] }];
set_property -dict { PACKAGE_PIN H24   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j2_5_to_36[12] }];
set_property -dict { PACKAGE_PIN J21   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j2_5_to_36[13] }];
set_property -dict { PACKAGE_PIN G24   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j2_5_to_36[14] }];
set_property -dict { PACKAGE_PIN H21   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j2_5_to_36[15] }];
set_property -dict { PACKAGE_PIN K27   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j2_5_to_36[16] }];
set_property -dict { PACKAGE_PIN M21   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j2_5_to_36[17] }];
set_property -dict { PACKAGE_PIN J27   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j2_5_to_36[18] }];
set_property -dict { PACKAGE_PIN L21   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j2_5_to_36[19] }];
set_property -dict { PACKAGE_PIN K23   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j2_5_to_36[20] }];
set_property -dict { PACKAGE_PIN N25   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j2_5_to_36[21] }];
set_property -dict { PACKAGE_PIN J23   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j2_5_to_36[22] }];
set_property -dict { PACKAGE_PIN N26   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j2_5_to_36[23] }];
set_property -dict { PACKAGE_PIN G26   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j2_5_to_36[24] }];
set_property -dict { PACKAGE_PIN M24   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j2_5_to_36[25] }];
set_property -dict { PACKAGE_PIN G27   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j2_5_to_36[26] }];
set_property -dict { PACKAGE_PIN L24   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j2_5_to_36[27] }];
set_property -dict { PACKAGE_PIN H25   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j2_5_to_36[28] }];
set_property -dict { PACKAGE_PIN G21   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j2_5_to_36[29] }];
set_property -dict { PACKAGE_PIN H26   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j2_5_to_36[30] }];
set_property -dict { PACKAGE_PIN G22   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j2_5_to_36[31] }];
set_property -dict { PACKAGE_PIN H23   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j2_37 }];

set_property -dict { PACKAGE_PIN K39   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j1_1 }];
set_property -dict { PACKAGE_PIN N38   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j1_2 }];
set_property -dict { PACKAGE_PIN K40   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j1_3_to_13[0] }];
set_property -dict { PACKAGE_PIN M39   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j1_3_to_13[1] }];
set_property -dict { PACKAGE_PIN J40   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j1_3_to_13[2] }];
set_property -dict { PACKAGE_PIN F40   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j1_3_to_13[3] }];
set_property -dict { PACKAGE_PIN J41   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j1_3_to_13[4] }];
set_property -dict { PACKAGE_PIN F41   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j1_3_to_13[5] }];
set_property -dict { PACKAGE_PIN P41   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j1_3_to_13[6] }];
set_property -dict { PACKAGE_PIN R40   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j1_3_to_13[7] }];
set_property -dict { PACKAGE_PIN N41   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j1_3_to_13[8] }];
set_property -dict { PACKAGE_PIN P40   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j1_3_to_13[9] }];
set_property -dict { PACKAGE_PIN M42   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j1_3_to_13[10] }];
set_property -dict { PACKAGE_PIN H39   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j1_14 }];
set_property -dict { PACKAGE_PIN L42   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j1_15 }];
set_property -dict { PACKAGE_PIN G39   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j1_16 }];
set_property -dict { PACKAGE_PIN H40   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j1_17_to_27[0] }];
set_property -dict { PACKAGE_PIN N39   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j1_17_to_27[1] }];
set_property -dict { PACKAGE_PIN H41   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j1_17_to_27[2] }];
set_property -dict { PACKAGE_PIN N40   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j1_17_to_27[3] }];
set_property -dict { PACKAGE_PIN M41   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j1_17_to_27[4] }];
set_property -dict { PACKAGE_PIN M36   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j1_17_to_27[5] }];
set_property -dict { PACKAGE_PIN L41   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j1_17_to_27[6] }];
set_property -dict { PACKAGE_PIN L37   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j1_17_to_27[7] }];
set_property -dict { PACKAGE_PIN K42   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j1_17_to_27[8] }];
set_property -dict { PACKAGE_PIN K37   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j1_17_to_27[9] }];
set_property -dict { PACKAGE_PIN J42   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j1_17_to_27[10] }];

set_property -dict { PACKAGE_PIN E34   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j3_1 }];
set_property -dict { PACKAGE_PIN H38   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j3_2 }];
set_property -dict { PACKAGE_PIN E35   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j3_3_to_13[0] }];
set_property -dict { PACKAGE_PIN G38   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j3_3_to_13[1] }];
set_property -dict { PACKAGE_PIN D35   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j3_3_to_13[2] }];
set_property -dict { PACKAGE_PIN J37   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j3_3_to_13[3] }];
set_property -dict { PACKAGE_PIN D36   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j3_3_to_13[4] }];
set_property -dict { PACKAGE_PIN J38   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j3_3_to_13[5] }];
set_property -dict { PACKAGE_PIN E33   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j3_3_to_13[6] }];
set_property -dict { PACKAGE_PIN B37   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j3_3_to_13[7] }];
set_property -dict { PACKAGE_PIN D33   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j3_3_to_13[8] }];
set_property -dict { PACKAGE_PIN B38   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j3_3_to_13[9] }];
set_property -dict { PACKAGE_PIN H33   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j3_3_to_13[10] }];
set_property -dict { PACKAGE_PIN B36   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j3_14 }];
set_property -dict { PACKAGE_PIN G33   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j3_15 }];
set_property -dict { PACKAGE_PIN A37   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j3_16 }];
set_property -dict { PACKAGE_PIN F34   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j3_17_to_27[0] }];
set_property -dict { PACKAGE_PIN E37   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j3_17_to_27[1] }];
set_property -dict { PACKAGE_PIN F35   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j3_17_to_27[2] }];
set_property -dict { PACKAGE_PIN E38   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j3_17_to_27[3] }];
set_property -dict { PACKAGE_PIN G32   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j3_17_to_27[4] }];
set_property -dict { PACKAGE_PIN C33   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j3_17_to_27[5] }];
set_property -dict { PACKAGE_PIN F32   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j3_17_to_27[6] }];
set_property -dict { PACKAGE_PIN C34   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j3_17_to_27[7] }];
set_property -dict { PACKAGE_PIN G36   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j3_17_to_27[8] }];
set_property -dict { PACKAGE_PIN B39   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j3_17_to_27[9] }];
set_property -dict { PACKAGE_PIN G37   IOSTANDARD LVCMOS18 } [get_ports { fmc1_j3_17_to_27[10] }];

set_property -dict { PACKAGE_PIN AD30   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j3_11 }];
set_property -dict { PACKAGE_PIN AG34   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j3_12 }];
set_property -dict { PACKAGE_PIN AA29   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j3_13_to_23[0] }];
set_property -dict { PACKAGE_PIN AE32   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j3_13_to_23[1] }];
set_property -dict { PACKAGE_PIN AA30   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j3_13_to_23[2] }];
set_property -dict { PACKAGE_PIN AE33   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j3_13_to_23[3] }];
set_property -dict { PACKAGE_PIN AB29   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j3_13_to_23[4] }];
set_property -dict { PACKAGE_PIN AF35   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j3_13_to_23[5] }];
set_property -dict { PACKAGE_PIN AC29   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j3_13_to_23[6] }];
set_property -dict { PACKAGE_PIN AF36   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j3_13_to_23[7] }];
set_property -dict { PACKAGE_PIN Y32   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j3_13_to_23[8] }];
set_property -dict { PACKAGE_PIN AE37   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j3_13_to_23[9] }];
set_property -dict { PACKAGE_PIN Y33   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j3_13_to_23[10] }];
set_property -dict { PACKAGE_PIN AF37   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j3_24 }];
set_property -dict { PACKAGE_PIN AB31   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j3_25 }];
set_property -dict { PACKAGE_PIN AG36   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j3_26 }];
set_property -dict { PACKAGE_PIN AB32   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j3_27_to_37[0] }];
set_property -dict { PACKAGE_PIN AH36   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j3_27_to_37[1] }];
set_property -dict { PACKAGE_PIN AC31   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j3_27_to_37[2] }];
set_property -dict { PACKAGE_PIN AC34   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j3_27_to_37[3] }];
set_property -dict { PACKAGE_PIN AD31   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j3_27_to_37[4] }];
set_property -dict { PACKAGE_PIN AD35   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j3_27_to_37[5] }];
set_property -dict { PACKAGE_PIN AA31   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j3_27_to_37[6] }];
set_property -dict { PACKAGE_PIN AB36   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j3_27_to_37[7] }];
set_property -dict { PACKAGE_PIN AA32   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j3_27_to_37[8] }];
set_property -dict { PACKAGE_PIN AB37   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j3_27_to_37[9] }];
set_property -dict { PACKAGE_PIN AE29   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j3_27_to_37[10] }];

set_property -dict { PACKAGE_PIN AD40   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j1_1 }];
set_property -dict { PACKAGE_PIN AB41   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j1_2_to_17[0] }];
set_property -dict { PACKAGE_PIN AD41   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j1_2_to_17[1] }];
set_property -dict { PACKAGE_PIN AB42   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j1_2_to_17[2] }];
set_property -dict { PACKAGE_PIN AF41   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j1_2_to_17[3] }];
set_property -dict { PACKAGE_PIN Y42   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j1_2_to_17[4] }];
set_property -dict { PACKAGE_PIN AG41   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j1_2_to_17[5] }];
set_property -dict { PACKAGE_PIN AA42   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j1_2_to_17[6] }];
set_property -dict { PACKAGE_PIN AK39   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j1_2_to_17[7] }];
set_property -dict { PACKAGE_PIN Y39   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j1_2_to_17[8] }];
set_property -dict { PACKAGE_PIN AL39   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j1_2_to_17[9] }];
set_property -dict { PACKAGE_PIN AA39   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j1_2_to_17[10] }];
set_property -dict { PACKAGE_PIN AJ42   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j1_2_to_17[11] }];
set_property -dict { PACKAGE_PIN W40   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j1_2_to_17[12] }];
set_property -dict { PACKAGE_PIN AK42   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j1_2_to_17[13] }];
set_property -dict { PACKAGE_PIN Y40   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j1_2_to_17[14] }];
set_property -dict { PACKAGE_PIN AL41   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j1_2_to_17[15] }];

set_property -dict { PACKAGE_PIN AB33   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j3_1 }];
set_property -dict { PACKAGE_PIN AF31   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j3_2 }];
set_property -dict { PACKAGE_PIN AC33   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j3_3 }];
set_property -dict { PACKAGE_PIN AF32   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j3_4 }];
set_property -dict { PACKAGE_PIN AD32   IOSTANDARD LVCMOS18 } [get_ports { fmc2_j3_5 }];
