$(document).ready(function() {
        $('#defaultForm').formValidation({
            message: 'This value is not valid',
            excluded: ':disabled',
            icon: {
                valid: 'glyphicon glyphicon-ok',
                invalid: 'glyphicon glyphicon-remove',
                validating: 'glyphicon glyphicon-refresh'
            },
            fields: {
                firstName: {
                    validators: {
                        notEmpty: {
                            message: 'The first name is required and cannot be empty'
                        },
                        stringCase: {
                            message: 'The first name must contain upper case characters only',
                            case: 'upper'
                        },
                        regexp: {
                            regexp: /^[A-Z\s]+$/i,
                            message: 'The first name can only consist of alphabetical characters and spaces'
                        }
                    }
                },
                lastName: {
                    validators: {
                        notEmpty: {
                            message: 'The last name is required and cannot be empty'
                        },
                        stringCase: {
                            message: 'The last name must contain upper case characters only',
                            case: 'upper'
                        },
                        regexp: {
                            regexp: /^[A-Z\s]+$/i,
                            message: 'The last name can only consist of alphabetical characters and spaces'
                        }
                    }
                },
                uname: {
                    message: 'The username is not valid',
                    validators: {
                        notEmpty: {
                            message: 'The username is required and cannot be empty'
                        },
                        stringLength: {
                            min: 6,
                            max: 30,
                            message: 'The username must be more than 6 and less than 30 characters long'
                        },
                        regexp: {
                            regexp: /^[a-zA-Z0-9_\.]+$/,
                            message: 'The username can only consist of alphabetical, number, dot and underscore'
                        }
                    }
                },
                email: {
                    validators: {
                        notEmpty: {
                            message: 'Email address is required and cannot be empty'
                        },
                        regexp: {
                            regexp: /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/,
                            message: 'The input is not a valid format email address'
                        }
                    }
                },
                password: {
                    validators: {
                        notEmpty: {
                            message: 'The password is required and can\'t be empty'
                        },
                        different: {
                            field: 'username',
                            message: 'The password cannot be the same as username'
                        },
                        regexp: {
                            regexp: /^(?=.*[a-zA-Z])(?=.*\d).{8,16}$/,
                            message: 'The passwords first character must be a letter, it must contain at least 8 characters and include at least one numeric digit'
                        }
                    }
                },
                confirmPassword: {
                    validators: {
                        notEmpty: {
                            message: 'The confirm password is required and can\'t be empty'
                        },
                        identical: {
                            field: 'passwd',
                            message: 'The password and its confirm are not the same'
                        }
                    }
                },
                agree: {
                    validators: {
                        notEmpty:{
                            message: 'You must agree with the terms and conditions'
                        }
                    }
                }
            }
        })
    });
