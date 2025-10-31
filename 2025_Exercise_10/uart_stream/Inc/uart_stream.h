/*
 * uart_stream.h
 *
 *  Created on: Oct 29, 2025
 *      Author: kaierih
 */

#ifndef INC_UART_STREAM_H_
#define INC_UART_STREAM_H_


#include "main.h"

void uart_send_block(UART_HandleTypeDef *huart, const float *samples, uint16_t count);

#endif /* INC_UART_STREAM_H_ */
