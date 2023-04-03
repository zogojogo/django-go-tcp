package util

import (
	"encoding/json"
	"net/http"
)

type TCPResponseDTO struct {
	Code    int         `json:"code"`
	Message string      `json:"message,omitempty"`
	Data    interface{} `json:"data,omitempty"`
}

func ResponseSuccessJSON(data interface{}, encoder *json.Encoder) error {
	response := TCPResponseDTO{
		Code: http.StatusOK,
		Data: data,
	}
	if err := encoder.Encode(response); err != nil {
		return err
	}
	return nil
}

func ResponseErrorJSON(statusCode int, err error, encoder *json.Encoder) error {
	response := TCPResponseDTO{
		Code:    statusCode,
		Message: err.Error(),
	}
	if err := encoder.Encode(response); err != nil {
		return err
	}
	return nil
}
