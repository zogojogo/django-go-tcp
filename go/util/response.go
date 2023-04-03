package util

import (
	"encoding/json"
	"entry_task/dto"
	"net/http"
)

func ResponseSuccessJSON(data interface{}, encoder *json.Encoder) error {
	response := dto.TCPResponseDTO{
		Code: http.StatusOK,
		Data: data,
	}
	if err := encoder.Encode(response); err != nil {
		return err
	}
	return nil
}

func ResponseErrorJSON(statusCode int, err error, encoder *json.Encoder) error {
	response := dto.TCPResponseDTO{
		Code:    statusCode,
		Message: err.Error(),
	}
	if err := encoder.Encode(response); err != nil {
		return err
	}
	return nil
}
