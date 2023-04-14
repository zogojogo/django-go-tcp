package domain

import "errors"

var ErrUserNotFound = errors.New("failed to get user, user not found")

var ErrInvalidCredentials = errors.New("failed to login, please check again your username or password")

var ErrUserAlreadyExists = errors.New("failed to register, user already exists")

var ErrFailedRegister = errors.New("failed to register")
