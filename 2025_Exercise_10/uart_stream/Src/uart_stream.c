/*
 * uart_stream.c
 *
 *  Created on: Oct 29, 2025
 *      Author: kaierih
 */

#include "uart_stream.h"


#define SIGNATURE  0xAA55AA55u

extern UART_HandleTypeDef huart2;

typedef struct __attribute__((packed)) {
    uint32_t magic;
    uint16_t count;
    uint8_t  bps;
    uint8_t  seq;
} uart_hdr_t;

static volatile uint8_t uart_busy = 0;
static volatile uint8_t phase     = 0;
static uart_hdr_t hdr;
static uint8_t seq = 0;

static const float *g_payload = NULL;
static uint32_t g_payload_bytes = 0;

void uart_send_block(UART_HandleTypeDef *huart, const float *samples, uint16_t count)
{
    if (uart_busy) return;
    g_payload       = samples;
    g_payload_bytes = count * sizeof(float);

    hdr.magic = SIGNATURE;
    hdr.count = count;
    hdr.bps   = sizeof(float);
    hdr.seq   = seq++;

    uart_busy = 1;
    phase = 1;
    HAL_UART_Transmit_DMA(huart, (uint8_t*)&hdr, sizeof(hdr));
}

void HAL_UART_TxCpltCallback(UART_HandleTypeDef *huart)
{
    if (huart != &huart2) return;

    if (phase == 1) {
        phase = 2;
        HAL_UART_Transmit_DMA(huart, (uint8_t*)g_payload, g_payload_bytes);
    } else {
        phase = 0;
        uart_busy = 0;
    }
}

